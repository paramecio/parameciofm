import os
import sys
from pathlib import Path
from paramecio.cromosoma.corefields import CharField
from paramecio.cromosoma.extraforms.fileform import FileForm
from paramecio.citoplasma import httputils
import traceback

from bottle import request
try:
    from PIL import Image
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
    
    
from uuid import uuid4
#from paramecio.cromosoma.extraforms.fileform import FileForm

class ImageField(CharField):
    
    def __init__(self, name, save_folder='media/upload/images', sizes=None, module=None, size=255, required=False):
        
        super().__init__(name, size, required)
        
        self.yes_prefix=True
        
        #self.name_form=FileForm
        
        self.thumbnail={'mini_': 150}
        
        self.yes_thumbnail=False
        
        self.default_quality_thumb=Image.ANTIALIAS
        
        # Is relative to media folder of paramecio
        
        #if module!=None:
        
        self.save_folder=save_folder
        
        self.file_related=True
        
        self.sizes=sizes
        
        self.name_form=FileForm
        self.extra_parameters=[self.save_folder]

        
    def change_folder(self, folder):
        
        pass
        
    def check(self, value):

        files_uploaded=request.files
        
        field_file=self.name+'_file'
        
        #if not change
        
        if not field_file in files_uploaded:

            if value=='':
                
                if self.model:
                    
                    if self.model.updated:
                        
                        old_reset=self.model.yes_reset_conditions
                        
                        self.model.yes_reset_conditions=False
                        
                        with self.model.select([self.name]) as cur:
                        
                            for arr_image in cur:
                                
                                if arr_image[self.name]!='':
                                    try:
                                        os.remove(arr_image[self.name])
                                    except:
                                        pass
                                
                                #if arr_image[self.name]!=save_file and arr_image[self.name]!='':
                                
                                #value=arr_image[self.name]
                        
                        self.model.yes_reset_conditions=old_reset
                self.txt_error='Field is empty'
                self.error=True
                
                return ''

            else:
                
                value=os.path.basename(value)
            
                return self.save_folder+'/'+value
            
        
        # Load image file
        
        file_bytecode=files_uploaded[field_file].file
        
        filename=files_uploaded[field_file].filename
        
        try:
            
            im=Image.open(file_bytecode)
            
        except IOError:
            
            self.error=True
            
            self.txt_error='Error, file not have a valid format'
            return ""

        real_width=im.size[0]
        real_height=im.size[1]
        
        if self.sizes:
            
            if 'maximum' in self.sizes:
                if self.sizes['maximum'][0]<real_width or self.sizes['maximum'][1]<real_height:
                    self.error=True
                    self.txt_error='Wrong size. Maximum size is '+str(self.sizes['maximum'][0])+'x'+str(self.sizes['maximum'][1])
                    im.close()
                    return ""
                    
            if 'minimum' in self.sizes:
                if self.sizes['minimum'][0]>real_width or self.sizes['minimum'][1]>real_height:
                    
                    self.error=True
                    self.txt_error='Wrong size. Minimum size is '+str(self.sizes['minimum'][0])+'x'+str(self.sizes['minimum'][1])
                    im.close()
                    return ""
            
            if 'resize' in self.sizes:
                
                height_t=0
                width_t=0
                
                if real_height<=self.sizes['resize'][1]:
                    height_t=self.sizes['resize'][1]
                
                if real_width>self.sizes['resize'][0]:
                    
                    width_t=self.sizes['resize'][0]
                    
                    if height_t==0:
                        ratio=(real_width/width_t)
                        height_t=round(real_height/ratio)
                        
                size=(width_t, height_t)
        
                if width_t>0 and height_t>0:
                    im.thumbnail(size, self.default_quality_thumb)

        format_image=im.format
        
        if format_image!='JPEG' and format_image!='GIF' and format_image!='PNG':
            
            self.error=True
            self.txt_error='Format is wrong. Requires JPEG or PNG formats'
            im.close()
            return ""
        
        # Create thumbnails and move file 
        
        realfilename, ext = os.path.splitext(filename)
        
        prefix=''
        
        if self.yes_prefix==True:
            prefix=uuid4().hex+'_'
        
        filename=prefix+filename
        
        save_file=self.save_folder+'/'+filename
        
        if self.yes_thumbnail:
            
            for name, width_t in self.thumbnail.items():
                
                im_thumb=im.copy()
                
                ratio=(real_width/width_t)
                height_t=round(real_height/ratio)
                
                size=(width_t, height_t)
                
                save_file_thumb=self.save_folder+'/'+name+filename
                
                im_thumb.thumbnail(size, self.default_quality_thumb)
                im_thumb.save(save_file_thumb, "JPEG")
                
                im_thumb.close()
                
        # Save file
        
        try:
            
        #Check if directory exists
            
            if not os.path.isdir(self.save_folder):
                
                # Try create if not
                
                try:
                    
                    p=Path(self.save_folder)
                        
                    p.mkdir(mode=0o755, parents=True)
                
                except:
                    im.close()
                    self.error=True
                    
                    self.txt_error='Error: cannot create the directory where save the image.Check permissions,'
                    return ""
            
            #files_uploaded[field_file].save(self.save_folder, overwrite=True)
            
            if os.path.isfile(save_file):
                
                os.remove(save_file)
            
            im.save(save_file)
            
            # Delete old files
            
            if self.model!=None:
                    
                if self.model.updated:
                
                    #old_conditions=self.model.conditions
                    
                    old_reset=self.model.yes_reset_conditions
                    
                    self.model.yes_reset_conditions=False
                    
                    with self.model.select([self.name]) as cur:
                        
                        for arr_image in cur:
                            
                            if arr_image[self.name]!=save_file and arr_image[self.name]!='':
                            
                                os.remove(arr_image[self.name])
                    
                    self.model.yes_reset_conditions=old_reset
                
                
                #self.model.conditions=old_conditions

            im.close()
            
            return save_file

        except:
            
            im.close()
            self.error=True
            self.txt_error='Error: cannot save the image file, Exists directory for save the file? '+traceback.format_exc()
            print(traceback.format_exc())
            return ""

    def show_formatted(self, value):
        
        return os.path.basename(value)
        
