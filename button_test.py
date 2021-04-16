import tkinter as tk
import pandas as pd
import random

class Application(tk.Frame):
    
    def __init__(self, dataFrame, ran_list, button_identities, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH,expand=True)
        counter=0
        #master.geometry("300x500")
        self.create_quit()
        for x in ran_list:
            self.create_genre_widgets(str(x), counter, button_identities)
            counter = counter+1
        self.create_inc(button_identities)
        self.create_exc(button_identities)
            
    def genre_clicked(self, m_title, button_identities, counter):
        user_input = str(m_title)
        output_list = []
        for x in range(0,7787):
            text = df.iat[x,genres_col]
            if user_input in text:
                output_list.append(df.iat[x,2])
        #print(output_list)
        #self.button.configure(bg="red")
        
        
            
        button_name = (button_identities[counter])
        button_name.configure(bg="red")
        
    #def update_list(self, output_list, current_list):
        #if current list is empty then equal to output list
        #else only keep same elements between lists
        
        #return current_list
        
    def create_inc(self, button_identity):
        self.button = tk.Button(self,text="Inclusive",fg="blue",command =lambda: self.inc_clicked(button_identity))
        
        self.button.grid(row = 8, column=2, pady=100)
        
        
    def inc_clicked(self, but_id):
        new_list = []
        
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = [] 
        
        for x in new_list:
            for y in range(0,7787):
                
                text = df.iat[y,genres_col]
                if (x in text) and (df.iat[y,2] not in output_list):
                    output_list.append(df.iat[y,2])
                    
        #print(output_list)
        self.show_titles(output_list)
        
    def create_exc(self, button_identity):
        self.button = tk.Button(self,text="Exclusive",fg="green",command =lambda: self.exc_clicked(button_identity))
        
        self.button.grid(row = 8, column=3, pady=100)     
        
    def exc_clicked(self, but_id):
        new_list = []
        
        for x in but_id:
            if x.cget("bg") == 'red':
                new_list.append(x.cget("text"))
                
        output_list = []         
      
        for y in range(0,7787):
            
            text = df.iat[y,genres_col]
            if all(x in text for x in new_list):
                output_list.append(df.iat[y,2])
                    
        #print(output_list)
        self.show_titles(output_list)
    

    def create_genre_widgets(self, m_title, counter, button_identities):
        
        self.button = tk.Button(self,text=str(m_title),command =lambda: self.genre_clicked(m_title,button_identities,counter))
        #self.button["text"] = str(m_title)
      
            
        self.button.grid(row= counter%6, column=counter%7)
            
        button_identities.append(self.button)
                    
    def create_quit(self):
     
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 8, column = 4, pady=100)
                
    def show_titles(self,shows_list):
        newWindow = tk.Toplevel(self.master)
        newWindow.title("10 Random Movies/TV Shows of Selected Items")
        new_counter = 0
        new_button_identities = []
        
        tk.Label(newWindow,text="Here are your shows").grid(row=0,column=0,pady=10)
        
        rand_list = random.sample(shows_list,10)
        #print(rand_list)
        
        for x in rand_list:
            self.create_show_titles(newWindow,x,new_counter,new_button_identities)
            new_counter +=1
            
    def create_show_titles(self,newWindow,show_title,counter,button_identity):
            newWindow.button = tk.Button(newWindow,text=str(show_title), command=lambda: self.show_title_info(newWindow,counter,button_identity))         
            newWindow.button.grid(row=(counter%2+1), column=counter%5)
            button_identity.append(newWindow.button)
    
    def show_title_info(self,newWindow,counter,button_identity):
        button_name = (button_identity[counter])
        button_name.configure(bg="red")
        
        info_text = ""
        
        for i in range(0,7787):
            title = df.iat[i,2]
            if (button_identity[counter].cget('text') == title):
                row = df.loc[i,:]
                for index, col in row.iteritems():
                    info_text = info_text + (str(index) + ': ' + str(col) + '\n')
                    
        infoWindow = tk.Toplevel(self.master)
        infoWindow.title("Information on Selected Show")
        tk.Label(infoWindow,text=("Here is your information:\n" + info_text)).pack()
        
def category_extraction(dataF, col_num):
#loop through pandas DataFrame column "col_num" and make a list of all entries
    list_items = []
    for x in range(0,7787):
        list_items.append(dataF.iat[x,col_num])
    
#creates a list of all the unique items from list of entries in col_num column
    category_list = []
    for x in range(0,len(list_items)):
        if (type(list_items[x]) != float):
            text = list_items[x]
            phrases = text.split(",")
            for y in range(0,len(phrases)):
                phrases[y] = phrases[y].lstrip()
                if phrases[y] not in category_list:
                    category_list.append(phrases[y])

    return(category_list)



df = pd.read_csv (r'https://raw.githubusercontent.com/kennedywaite/CLPS0950FinalProject/main/netflix_titles.csv')
        
genres_col = 10
        
genre_list = category_extraction(df,genres_col)
current_list = []
button_identities = [] 

root = tk.Tk()
app = Application(df, genre_list, button_identities, master=root)
app.mainloop()

