from gi.repository import Clutter, ClutterGst
from xml.etree import cElementTree as ET
import sys
import time

def timeToMS(text):
    if text[-1] == 's':
        return int(text[:-1]) * 1000

class layout_rootlayout():
    def __init__(self, backgroundColor=None, height=None, width=None):
        self._backgroundColor = backgroundColor
        self._height = height
        self._width  = width

        self.stage = None

    def setFromAttrib(self, attrib):
        if 'backgroundColor' in attrib:
            self._backgroundColor = attrib['backgroundColor']
        if 'height' in attrib:
            self._height = int(attrib['height'])
        if 'width' in attrib:
            self._width = int(attrib['width'])

    def __str__(self):
        return str({'backgroundColor': self_backgroundColor,
                    'height': self._height,
                    'width': self._width})

    def clutter(self, stage):
        self.stage = stage
        self.stage.set_size(self._width, self._height)
        
        if self._backgroundColor:
            color = Clutter.Color.new(0, 0, 0, 1.0)
            color.from_string(self._backgroundColor)
            self.stage.set_color(color)
 
class layout_region():
    def __init__(self, backgroundColor=None, backgroundOpacity=1.0, bottom=None, fit='hidden', height=None, left=None, regionName='', right=None, showBackground='always', top=None, width=None, zindex=None):
        self._backgroundColor = backgroundColor
        self._backgroundOpacity = backgroundOpacity
        self._bottom = bottom
        self._fit = fit
        self._height = height
        self._left = left
        self._regionName = regionName
        self._right = right
        self._showBackground = showBackground
        self._top = top
        self._width = width
        self._zindex = zindex

        self.stage = None

    def setFromAttrib(self, attrib):
        if 'backgroundColor' in attrib:
            self._backgroundColor = attrib['backgroundColor']
        if 'backgroundOpacity' in attrib:
            self._backgroundOpacity = float(attrib['backgroundOpacity'])
        if 'bottom' in attrib:
            self._bottom = int(attrib['bottom'])
        if 'fit' in attrib:
            self._fit = attrib['fit']
        if 'height' in attrib:
            self._height = int(attrib['height'])
        if 'left' in attrib:
            self._left = int(attrib['left'])
        if 'regionName' in attrib:
            self._regionName = attrib['regionName']
        if 'right' in attrib:
            self._right = int(attrib['right'])
        if 'showBackground' in attrib:
            self._showBackground = attrib['showBackground']
        if 'top' in attrib:
            self._top = int(attrib['top'])
        if 'width' in attrib:
            self._width = int(attrib['width'])
        if 'z-index' in attrib:
            self._zindex = int(attrib['z-index'])

    def __str__(self):
        return str({'backgroundColor': self._backgroundColor,
                'backgroundOpacity': self._backgroundOpacity,
                'bottom': self._bottom,
                'fit': self._fit,
                'height': self._height,
                'left': self._left,
                'regionName': self._regionName,
                'right': self._right,
                'showBackground': self._showBackground,
                'top': self._top,
                'width': self._width,
                'z-index': self._zindex})

    def clutter(self, stage):
        self.stage = Clutter.Actor()
        if self._width and self._height:
            self.stage.set_size(int(self._width), int(self._height))

        if self._backgroundColor:
            color = Clutter.Color.new(0, 0, 0, 1.0)
            color.from_string(self._backgroundColor)
            self.stage.set_background_color(color)

        if self._backgroundOpacity:
            self.stage.set_opacity(self._backgroundOpacity * 255)

        if self._top and self._left:
            self.stage.set_position(self._left, self._top)

        stage.add_actor(self.stage)
        self.stage.show()

class body_ref():
    def __init__(self, src=None, type=None, region=None, erase='whenDone'):
        self._src = src
        self._type = type


class timing():  
    def __init__(self, begin=None, dur=None, end=None, repeatCount=None, repeatDur=None, repeat=None, fill=None, restart=None):
        self._begin = begin
        self._dur = dur
        self._end = end
        self._repeatCount = repeatCount
        self._repeatDur = repeatDur
        self._repeat = repeat
        self._fill = fill
        self._restart = restart

    def setFromAttrib(self, attrib):
        if 'begin' in attrib:
            self._begin = timeToMS(attrib['begin'])
        if 'dur' in attrib:
            self._dur = timeToMS(attrib['dur'])
        if 'end' in attrib:
            self._end = timeToMS(attrib['end'])
        if 'repeatCount' in attrib:
            self._repeatCount = float(attrib['repeatCount'])
        if 'repeatDur' in attrib:
            self._repeatDur = timeToMS(attrib['repeatDur'])
        if 'repeat' in attrib:
            self._repeat = attrib['repeat']
        if 'fill' in attrib:
            self._fill = attrib['fill']
        if 'restart' in attrib:
            self._restart = attrib['restart']

class body_par(timing):
    def __init__(self, begin=None, dur=None, end=None, repeatCount=None, repeatDur=None, repeat=None, fill=None, restart=None):
        self._items = []
        timing.__init__(self, begin, dur, end, repeatCount, repeatDur, repeat, fill, restart)
    
    def add(self, smilelement):
        self._items.add(smilelement)

    def setItems(self, items):
        self._items = items

    def setFromAttrib(self, attrib):
        timing.setFromAttrib(self, attrib)

class body_seq(timing):
    def __init__(self, begin=None, dur=None, end=None, repeatCount=None, repeatDur=None, repeat=None, fill=None, restart=None):
        self._items = []
        self._index = 0
        timing.__init__(self, begin, dur, end, repeatCount, repeatDur, repeat, fill, restart)

        self._after = None

    def add(self, smilelement):
        self._items.add(smilelement)
    
    def setItems(self, items):
        self._items = items
    
    def setFromAttrib(self, attrib):
        timing.setFromAttrib(self, attrib)

    def start(self, after=None):
        self._after = after
        self._items[self._index].start(self.advance)

    def advance(self, _data=None):
        self._index += 1
        if self._index >= len(self._items):
            if self._after is not None:
                self._after()
        else:
            self._items[self._index].start(self.advance)
            self._items[self._index - 1].clutter_destroy()

class body_excl(body_par):
    def __init__(self, begin=None, dur=None, end=None, repeatCount=None, repeatDur=None, repeat=None, fill=None, restart=None):
        body_par.__init__(self, begin=None, dur=None, end=None, repeatCount=None, repeatDur=None, repeat=None, fill=None, restart=None)


class body_ref(timing):
    def __init__(self, tag, src=None, erase='whendone', mediaRepeat='preserve', sensitivity='opaque', region=None, begin=None, dur=None, end=None, repeatCount=None, repeatDur=None, repeat=None, fill=None, restart=None):
        self._tag = tag
        self._src = src
        self._erase = erase
        self._mediaRepeat = mediaRepeat
        self._sensitivity = sensitivity
        self._region = region

        self.actor = None
        self.clone = []
        self._after = None
        
        timing.__init__(self, begin, dur, end, repeatCount, repeatDur, repeat, fill, restart)

    def setFromAttrib(self, attrib):
        if 'src' in attrib:
            self._src = attrib['src']
        if 'erase' in attrib:
            self._erase = attrib['erase']
        if 'mediaRepeat' in attrib:
            self._mediaRepeat = attrib['mediaRepeat']
        if 'sensitivity' in attrib:
            self._sensitivity = attrib['sensitivity']
        if 'region' in attrib:
            self._region = attrib['region']

        timing.setFromAttrib(self, attrib)

    def start(self, after=None):
        self._after = after
        self.clutter()

    def clutter_destroy(self):
        self.actor.destroy()
        for clone in self.clone:
            clone.destroy()

    def clutter(self):
        if self.actor is None:
            if self._tag == 'img':
                self.actor = Clutter.Texture()
                self.actor.set_from_file(self._src)

            elif self._tag == 'video':
                self.actor = ClutterGst.VideoTexture()
                self.actor.set_seek_flags(ClutterGst.SeekFlags(1))
                self.actor.set_uri(self._src)
                self.actor.connect("eos", self._after)
            
            if self._region in region_names:
                parent = False
                for region in region_names[self._region]:
                    if not parent:
                        region.stage.add_actor(self.actor)
                        parent = True
                    else:
                        clone = Clutter.Clone.new(self.actor)
                        region.stage.add_actor(clone)
                        self.clone.append(clone)
            elif self._region in region_ids:
                region_ids[self._region].stage.add_actor(self.actor)
            else:
                stage.add_actor(self.actor)
        
        if self._tag == 'img':
            Clutter.threads_add_timeout(0, self._dur, self._after, None)
        elif self._tag == 'video':
            self.actor.set_progress(0.0)
            self.actor.set_playing(True)

        self.actor.show()

def parselist(item, xml):
    items = []
    for element in xml:
        if element.tag in ['excl', 'seq', 'par']:
            if element.tag == 'excl':
                item2 = body_excl()
            elif element.tag == 'par':
                item2 = body_par()
            elif element.tag == 'seq':
                item2 = body_seq()

            parselist(item2, element)
            
        elif element.tag in ['ref', 'animation', 'audio', 'img', 'text', 'textstream', 'video']:
            item2 = body_ref(element.tag)

        item2.setFromAttrib(element.attrib)
        items.append(item2)

    item.setItems(items)

region_ids = {}
region_names = {}

xml = ET.parse(sys.argv[1])
root = xml.find('./head/layout/root-layout')
smil_rootlayout = layout_rootlayout()
smil_rootlayout.setFromAttrib(root.attrib)

Clutter.init(sys.argv)
ClutterGst.init(sys.argv)

stage = Clutter.Stage.get_default()
stage.set_title("SMIL")

smil_rootlayout.clutter(stage)

for region in xml.findall('./head/layout/region'):
    smil_region = layout_region()
    smil_region.setFromAttrib(region.attrib)

    if '{http://www.w3.org/XML/1998/namespace}id' in region.attrib:
        region_ids[region.attrib['{http://www.w3.org/XML/1998/namespace}id']] = smil_region
    
    if 'regionName' in region.attrib:
        if region.attrib['regionName'] in region_names:
            region_names[region.attrib['regionName']].append(smil_region)
        else:
            region_names[region.attrib['regionName']] = [smil_region]

    smil_region.clutter(stage) 


element = xml.find('./body')
body = body_seq()
body.setFromAttrib(element.attrib)
parselist(body, element)
body.start()

stage.show()
Clutter.main()
