import os
import sys
from pathlib import Path
from paramecio.cromosoma.corefields import CharField
from paramecio.citoplasma.httputils import GetPostFiles
try:
    from PIL import Image
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
    
    
from uuid import uuid4
#from paramecio.cromosoma.extraforms.fileform import FileForm

class ImageField(CharField):
    
    def __init__(self, name, save_folder='media/upload/images', module=None, size=255, required=False):
        
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
        
    def change_folder(self, folder):
        
        pass
        
    def check(self, value):
        
        #GetPostFiles.obtain_files()
        
        field_file=self.name+'_file'
        
        if not field_file in GetPostFiles.files:
            
            self.error=True
            self.txt_error='Error, no exists image file'
            return ""
        # Load image file
        
        file_bytecode=GetPostFiles.files[field_file].file
        
        filename=GetPostFiles.files[field_file].filename
        
        try:
            
            im=Image.open(file_bytecode)
            
        except IOError:
            
            self.error=True
            
            self.txt_error='Error, file not exists'
            return ""
        
        format_image=im.format
        
        if format_image!='JPEG' and format_image!='GIF' and format_image!='PNG':
            
            self.error=True
            self.txt_error='Format is wrong. Requires JPEG, GIF or PNG formats'
            return ""
        
        # Create thumbnails and move file 
        
        realfilename, ext = os.path.splitext(filename)
        
        prefix=''
        
        if self.yes_prefix==True:
            prefix=uuid4().hex+'_'
        
        filename=prefix+filename
        
        save_file=self.save_folder+'/'+filename
        
        if self.yes_thumbnail:
        
            real_width=im.size[0]
            real_height=im.size[1]
            
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
                    
                    self.error=True
                    self.txt_error='Error: cannot create the directory where save the image.Check permissions,'
                    return ""
            
            #GetPostFiles.files[field_file].save(self.save_folder, overwrite=True)
            
            if os.path.isfile(save_file):
                
                os.remove(save_file)
            
            im.save(save_file)
            
            # Delete old files
            
            if self.model!=None:
                
                old_reset=self.model.yes_reset_conditions
                
                self.model.yes_reset_conditions=False
                
                cur=self.model.select([self.name])
                
                for arr_image in cur:
                    
                    if arr_image[self.name]!=save_file:
                    
                        os.remove(arr_image[self.name])
                
                self.model.yes_reset_conditions=old_reset
            
            return save_file

        except:
            
            self.error=True
            self.txt_error='Error: cannot save the image file, Exists directory for save the file?'
            return ""

    def show_formatted(value):
        
        return os.path.basename(value)
        
