import os ,shutil, time,sys
from distutils.dir_util import copy_tree
import tkinter as tk
import pygame
from tkinter import  filedialog,messagebox,LabelFrame,Label,Button
from PIL import Image

class App(tk.Tk):
    
    file_extn = ('.jpg','.jpeg','.png')
    
    def __init__(self, *args, **kwargs):


        pygame.mixer.init()
        t_pth = os.getcwd()
        pygame.mixer.music.load(r'{}\music\bg.mp3'.format(t_pth))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(loops=-1)

        # root initialization
        super().__init__(*args, **kwargs)

        self.resizable(False,False)   
        
        self.x=self.winfo_screenwidth()//2
        self.y=self.winfo_screenheight()//2
        self.xx = (self.x-(self.x//2))//2
        self.yy = (self.y-(self.y//2))//2 
        self.iconbitmap('favicon.ico')
        self.title('Automate Watermark on Images')
        self.focus()
        self.geometry('{}x{}+{}+{}'.format(self.x,self.y, self.xx , self.yy))

        # Heading
        self.lbl_head = LabelFrame(self,bg='#005082',fg="#fff",relief=tk.RAISED)
        self.lbl_head.grid(row=0,padx=self.xx//1.88,pady= self.yy//8)
        Label(
            self.lbl_head,bg='#005082',fg="#fff",
            text='RadientBrain Watermark System',
            font=('TkDefaultFont', 16)
        ).grid(row=0,padx=self.xx//2,pady= self.yy//8)
        
        # Source DIR
        self.lbl_src = LabelFrame(self,bg='#005082',fg="#fff", text='Choose Images Source Directory',relief=tk.RIDGE,labelanchor="n")
        self.lbl_src.grid(row=1,column=0,padx=self.xx//4,pady= self.yy//8)

        self.src_dir = Button(self.lbl_src,bg='#005082',fg="#fff", text='Open',
                                     command=self.open_src,relief=tk.RAISED)
        self.src_dir.grid(sticky="n e w s", row=0, padx=self.xx//2,pady= self.yy//4)


        # Watermark DIR
        self.wtrmk = LabelFrame(self,bg='#005082',fg="#fff", text='Choose Watermark Image',relief=tk.RIDGE,labelanchor="n")
        self.wtrmk.grid(row=2,column=0,padx=self.xx//4,pady= self.yy//8)
        self.wtrmk_btn = Button(self.wtrmk,bg='#005082',fg="#fff", text='Open',
                                     command=self.open_wtrmk_dir,relief=tk.RAISED)
        self.wtrmk_btn.grid(sticky="n e w s", row=0, padx=self.xx//2,pady= self.yy//4)


        #Start Process
        self.lbl_start = LabelFrame(self,bg='#005082',fg="#fff",relief=tk.RIDGE,labelanchor="n",bd=0)
        self.lbl_start.grid(row=3,column=0)
        self.start_btn = Button(self.lbl_start,bg='#005082',fg="#fff", text='Start Process',
                                     command=self.start_process,relief=tk.RAISED)
        self.start_btn.grid(sticky="n e w s", row=0,column=0,padx=self.xx//32)

        #Next Process
        self.next_btn = Button(self.lbl_start,bg='#005082',fg="#fff", text='Next Process',
                                     command=self.next_process,relief=tk.RAISED)
        self.next_btn.grid(sticky="n e w s", row=0,column=1,padx=self.xx//32)

        try:
            os.remove(f"{os.getcwd()}/wtrmk_dir/logo.png")


        except Exception as e:
            self.next_process()

        try:
            folder = f"{os.getcwd()}/dst_photos"
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        except Exception as e:
            self.next_process()

    def next_process(self):

        try:
            self.progress_lbl.config(text="",width=40,height=2)
            os.remove(f"{os.getcwd()}/wtrmk_dir/logo.png")
        except Exception as e:
            # print("inside next process")
            pass

        try:
            folder = f"{os.getcwd()}/dst_photos"
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        except Exception as e:
            # print("inside next process")
            pass


    def start_process(self):
        global Flag


        # #Label for progress
        self.lbl_progress = LabelFrame(self,bg='#005082',bd=0,labelanchor="n")
        self.lbl_progress.grid(row=4,column=0,padx=self.xx//4,pady = self.yy//32)
        self.progress_lbl= Label(self.lbl_progress,bg='#005082',fg="#fff", text='Task in Progress...',width=40,height=2)
        self.progress_lbl.grid(sticky="n e w s", row=0)
        self.update()


        automate_it = AutomatePhotoshopWatermark(App)
        automate_it.run()
        
        if(Flag):
            time.sleep(1)
            self.progress_lbl.config(text="Please select a valid Image source directory first!\nThis might be empty!",width=40,height=2)
            Flag=0
        else:
            # self.progress_lbl.grid_remove()
            self.progress_lbl.config(text='Task Completed!',width=40,height=2)

        

    def open_src(self):
        self.src_file_dir = filedialog.askdirectory(initialdir=os.getcwd())
        self.src_photos_dir = f"{os.path.dirname(os.path.abspath(__file__))}/{'src_photos'}"
        if(self.src_file_dir==''):
            messagebox.showinfo("No Directory Selected","Please select a directory!")
        else:
            copy_tree(self.src_file_dir, self.src_photos_dir)

    def open_wtrmk_dir(self):
        
        self.wtrmk_from_user = filedialog.askopenfilename(initialdir=os.getcwd())
        # print(self.wtrmk_from_user)
        self.dstn_photos_dir = f"{os.path.dirname(os.path.abspath(__file__))}/{'wtrmk_dir'}"
        if(self.wtrmk_from_user==""):
            messagebox.showinfo("No Watermark Image Selected","Please select an Image as watermark!")
        else:
            try:
                shutil.copy(self.wtrmk_from_user, self.dstn_photos_dir)
                self.update()
                os.rename(f"{os.getcwd()}/wtrmk_dir/{os.path.basename(self.wtrmk_from_user)}",f"{os.getcwd()}/wtrmk_dir/logo.png")
            except Exception as e:
                if sys.hexversion < 0x03000000:
                    if isinstance(e, shutil.Error) and "same file" in str(e):
                        pass
                elif isinstance(e, shutil.SameFileError):
                        pass
                else:
                    if "file already exists" in str(e):
                        messagebox.showerror("Error!","Please Click on Next button to proceed!")
                raise # Must be another error 
            

    def run(self):
        self.mainloop()


class AutomatePhotoshopWatermark(App):
    def __init__(self, *args, **kwargs) :
        # print(self.app.open_src.src_file_dir)
        self.file_extn = App.file_extn
        self.src_photos = f"{os.path.dirname(os.path.abspath(__file__))}/{'src_photos'}"
        self.dst_photos = f"{os.path.dirname(os.path.abspath(__file__))}/{'dst_photos'}"

        try:
            self.wtrmk_img = Image.open(f"{os.getcwd()}/wtrmk_dir/logo.png").convert("RGBA")

            self.wtrmk_img_width = self.wtrmk_img.width
            self.wtrmk_img_height = self.wtrmk_img.height
        except Exception as e:
            # print('logo file not there')
            pass
    
    def run(self):
        global Flag
        self.pics = self.outsource_files()
        if(len(self.pics) == 0):
            Flag=1
        else:
            self.put_wtrmk(self.pics)
            self.clear_src_photos_dir(self.pics)

    def clear_src_photos_dir(self,f_name):
        for imgs in f_name:
            os.remove(f"{self.src_photos}/{imgs}")

    def outsource_files(self):
        return [f for f in [f for f in os.listdir(self.src_photos) if os.path.isfile(os.path.join(self.src_photos,f)) ] if f.endswith(self.file_extn)]


    def put_wtrmk(self,f_name):
        for imgs in f_name:
            self.put_logo(imgs)

    def put_logo(self,f_name):
        self.final_img = Image.open(f'{self.src_photos }/{f_name}')
        self.final_img_width = self.final_img.width
        self.final_img_height = self.final_img.height
        self.final_img.paste( self.wtrmk_img,(int((self.final_img_width-self.wtrmk_img_width)/2),int((self.final_img_height-self.wtrmk_img_height)/2)),self.wtrmk_img )


        self.final_img.save(f"{self.dst_photos}/modified_{f_name}")



def main():
    app=App()
    app['bg'] = '#005082'
    auto_wtrmk = AutomatePhotoshopWatermark()
    app.run()


if __name__ == "__main__":
    #for progress label
    Flag = 0
    main()