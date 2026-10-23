// Draw one line of Devanagari (or any text) with CoreText, which shapes conjuncts correctly.
// usage: deva <font> <size> <r> <g> <b> <out.png> <text>
import AppKit

let a = CommandLine.arguments
guard a.count >= 8 else { FileHandle.standardError.write("usage: deva font size r g b out text\n".data(using: .utf8)!); exit(2) }
let size = CGFloat(Double(a[2])!)
let font = NSFont(name: a[1], size: size) ?? NSFont(name: "DevanagariMT", size: size) ?? NSFont.systemFont(ofSize: size)
let col = NSColor(srgbRed: CGFloat(Double(a[3])! / 255), green: CGFloat(Double(a[4])! / 255), blue: CGFloat(Double(a[5])! / 255), alpha: 1)
let s = NSAttributedString(string: a[7], attributes: [.font: font, .foregroundColor: col])
let line = CTLineCreateWithAttributedString(s)
var asc: CGFloat = 0, desc: CGFloat = 0, lead: CGFloat = 0
let w = CTLineGetTypographicBounds(line, &asc, &desc, &lead)
let pad: CGFloat = 10
let W = Int(ceil(w + pad * 2)), H = Int(ceil(asc + desc + pad * 2))
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.textPosition = CGPoint(x: pad, y: pad + desc)
CTLineDraw(line, ctx)
let rep = NSBitmapImageRep(cgImage: ctx.makeImage()!)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[6]))
