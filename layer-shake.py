#!/usr/bin/env python
import sys,os,math,traceback
import random
from gimpfu import *
    
def shake_layer(image, source, count, intensity, frameDuration, namePattern):

    image.undo_group_start()
    savedSel=None
    try:
        formatValues={}
        formatValues['sourceName']=source.name
        formatValues['count']=count
        
        savedSel=pdb.gimp_selection_save(image)
        pdb.gimp_selection_none(image)
        new_name = namePattern.format(sourceName=formatValues['sourceName'],count=0)
        new_name += " ({duration:d}ms)".format(duration=int(frameDuration))
        pdb.gimp_item_set_name(source, new_name)
        for i in range(int(count)):
            transform = source.copy()
            new_name = namePattern.format(sourceName=formatValues['sourceName'],count=i+1)
            new_name += " ({duration:1d}ms)".format(duration=int(frameDuration))
            pdb.gimp_item_set_name(transform, new_name)
            rand_x = random.randint(-intensity, intensity)
            rand_y = random.randint(-intensity, intensity)
            pdb.gimp_item_transform_translate(transform, rand_x, rand_y)
            image.add_layer(transform,0)
            
    except Exception as e:
        pdb.gimp_message(e.args[0])
        print traceback.format_exc()
    if savedSel:
        pdb.gimp_image_select_item(image,CHANNEL_OP_REPLACE,savedSel)
        image.remove_channel(savedSel)
        
    image.undo_group_end()
    

### Registrations
author='Eric Schneider'
year='2019'
desc='Create multiple translated layers for a shake effect'
whoiam='\n'+os.path.abspath(sys.argv[0])

register(
    'shake-layer',
    desc+whoiam,desc,author,author,year,'Add Shake...',
    '*',
    [
        (PF_IMAGE,      'image',            'Input image',      None),
        (PF_DRAWABLE,   'source',           'Input layer',      None),
        (PF_SPINNER,    'count',            'Number of Frames', 12, (1,1000,1)),
        (PF_SPINNER,    'intensity',        'Intensity',        5, (1,1000,1)),
        (PF_SPINNER,    'frameDuration',    'Frame duration',   30, (1,4000,10)),
        (PF_STRING,     'namePattern',      'Layer name',       '{sourceName}-{count:03d} (replace)')
    ],
    [],
    shake_layer,
    menu='<Image>/Layer/Transform'
)

main()
