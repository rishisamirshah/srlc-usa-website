// faces <image>... -> one JSON line per image: {"file","w","h","faces":[[x,y,w,h,conf],...]}
// Coordinates are top-left normalized. Runs on the whole image plus overlapping
// tiles (small faces in group shots are missed at full size), then merges.
import Foundation
import Vision
import AppKit

func detect(_ cg: CGImage) -> [(CGRect, Float)] {
    let req = VNDetectFaceRectanglesRequest()
    if #available(macOS 12.0, *) { req.revision = VNDetectFaceRectanglesRequestRevision3 }
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    return (req.results ?? []).map { ($0.boundingBox, $0.confidence) }
}
// a plain 8-bit RGBA copy: some 16-bit and VP8 sources crash Vision on cropped tiles
func redraw(_ src: CGImage) -> CGImage? {
    guard let ctx = CGContext(data: nil, width: src.width, height: src.height, bitsPerComponent: 8, bytesPerRow: 0,
                              space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return nil }
    ctx.draw(src, in: CGRect(x: 0, y: 0, width: src.width, height: src.height))
    return ctx.makeImage()
}
func iou(_ a: CGRect, _ b: CGRect) -> CGFloat {
    let i = a.intersection(b); if i.isNull { return 0 }
    let ia = i.width * i.height
    return ia / min(a.width * a.height, b.width * b.height)
}

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let src = img.cgImage(forProposedRect: nil, context: nil, hints: nil),
          let cg = redraw(src) else {
        print("{\"file\":\"\(path)\",\"error\":\"unreadable\"}"); continue
    }
    let W = CGFloat(cg.width), H = CGFloat(cg.height)
    var found: [(CGRect, Float)] = []  // top-left normalized
    for (b, c) in detect(cg) { found.append((CGRect(x: b.minX, y: 1 - b.maxY, width: b.width, height: b.height), c)) }
    for n in [2, 3] {
        let tw = (W * 2 / CGFloat(n + 1)).rounded(.down), th = (H * 2 / CGFloat(n + 1)).rounded(.down)
        for i in 0..<n { for j in 0..<n {
            let ox = ((W - tw) * CGFloat(i) / CGFloat(n - 1)).rounded(.down), oy = ((H - th) * CGFloat(j) / CGFloat(n - 1)).rounded(.down)
            guard let tile = cg.cropping(to: CGRect(x: ox, y: oy, width: tw, height: th)) else { continue }
            for (b, c) in detect(tile) {
                let r = CGRect(x: (ox + b.minX * tw) / W, y: (oy + (1 - b.maxY) * th) / H, width: b.width * tw / W, height: b.height * th / H)
                found.append((r, c))
            }
        } }
    }
    var keep: [(CGRect, Float)] = []
    for f in found.sorted(by: { $0.1 > $1.1 }) where f.1 >= 0.5 {
        if !keep.contains(where: { iou($0.0, f.0) > 0.4 }) { keep.append(f) }
    }
    let faces = keep.map { String(format: "[%.4f,%.4f,%.4f,%.4f,%.2f]", $0.0.minX, $0.0.minY, $0.0.width, $0.0.height, $0.1) }
    print("{\"file\":\"\(path)\",\"w\":\(cg.width),\"h\":\(cg.height),\"faces\":[\(faces.joined(separator: ","))]}")
}
