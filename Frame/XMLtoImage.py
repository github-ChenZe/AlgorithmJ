from jpype import *
import jpype as jp
import PIL.Image as Image
import io


class XMLtoImage(object):
    def __init__(self):
        print """init"""
        classpath = "/Users/zechen/Intellij/AlgorithmGraphic/out/artifacts/AlgorithmGraphic_jar/AlgorithmGraphic.jar"
        jp.startJVM(jp.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % classpath)
        reader = jp.JPackage("XMLReader").XMLReader
        self.reader = reader

    def convert(self, xml):
        print "CONVERSION"
        arr = self.reader.newBytes(len(xml))
        print "IMAGE"
        for i in range(0, len(xml)):
            arr[i] = JByte(ord(xml[i]))
        rgba = self.reader.toDiagram(arr)
        length = len(rgba)
        b = bytearray(length)
        for i in range(0, length):
            b[i] = (rgba[i] & 0xff)
        image = Image.open(io.BytesIO(b))
        return image

    def sample(self):
        return self.convert("""<?xml version="1.0" encoding="utf-8" ?>
        <table>
            <row>
                <table>
                    <row>
                        <cell>First</cell>
                        <cell>Second</cell>
                    </row>
                </table>
                <cell>Python</cell>
            </row>
            <row>
                <cell>Speed</cell>
                <cell>Slow</cell>
            </row>
        </table>""")


# Convector = XMLtoImage()


def sample():
    return XMLtoImage().convert("""<?xml version="1.0" encoding="utf-8" ?>
    <table>
        <row>
            <table>
                <row>
                    <cell>First</cell>
                    <cell>Second</cell>
                </row>
            </table>
            <cell>Python</cell>
        </row>
        <row>
            <cell>Speed</cell>
            <cell>Slow</cell>
        </row>
    </table>""")


if __name__ == '__main__':
    sample().show()
