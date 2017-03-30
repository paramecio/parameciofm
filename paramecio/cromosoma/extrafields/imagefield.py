import os
import sys
from pathlib import Path
from paramecio.cromosoma.corefields import CharField
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
                                    os.remove(arr_image[self.name])
                                
                                #if arr_image[self.name]!=save_file and arr_image[self.name]!='':
                                
                                #value=arr_image[self.name]
                        
                        self.model.yes_reset_conditions=old_reset
                
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
            
            self.txt_error='Error, file not exists'
            return ""
            
        real_width=im.size[0]
        real_height=im.size[1]

        if self.sizes:
            if 'maximum' in self.sizes:
                if self.sizes.size['maximum'][0]<real_width or self.sizes.size['maximum'][1]<real_height:
                    self.error=True
                    self.txt_error='Size is wrong. Maximum size is '+str(self.sizes.size['maximum'][0])+'x'+str(self.sizes.size['maximum'][1])
                    im.close()
                    return ""
                    
            if 'minimum' in self.sizes:
                if self.sizes.size['minimum'][0]<real_width or self.sizes.size['minimum'][1]<real_height:
                    self.error=True
                    self.txt_error='Size is wrong. Minimum size is '+str(real_width)+'x'+str(real_height)
                    im.close()
                    return ""
        

        format_image=im.format
        
        if format_image!='JPEG' and format_image!='GIF' and format_image!='PNG':
            
            self.error=True
            self.txt_error='Format is wrong. Requires JPEG, GIF or PNG formats'
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

    def show_formatted(value):
        
        return os.path.basename(value)
        
