import datetime,sqlite3,sys,os
db=sqlite3.connect('db.db')
cdb=db.cursor()
cdb.execute('create table if not exists first(nm,img,prc,nf)')
cdb.execute('create table if not exists second(nm,img,prc,nf)')
cdb.execute('create table if not exists side(nm,img,prc,nf)')
cdb.execute('create table if not exists fruit(nm,img,prc,nf)')
cdb.execute('create table if not exists sweet(nm,img,prc,nf)')
cdb.execute('create table if not exists drink(nm,img,prc,nf)')
cdb.execute('create table if not exists cart(id integer primary key autoincrement,nm,prc)')
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
class app(MDApp):
    def build(self):
        Window.maximize()
        Window.clearcolor=(1,1,1,1)
        self.page=BoxLayout(orientation='vertical')
        self.top=BoxLayout(size_hint_y=None,height=200,spacing=200)
        self.top.add_widget(Label())
        self.top.add_widget(Button(background_normal='images/logo.jpg',width=50,height=50))
        self.dd_lang=DropDown()
        self.langs=['ENGLISH','ESPANOL','ITALIANO']
        for lang in self.langs:
            self.b_lang=Button(text=lang,on_release=lambda b_lang:self.dd_lang.select(b_lang.text),size_hint_y=None,height=50)
            self.dd_lang.add_widget(self.b_lang)
        self.m_lang=Button(text='LANGUAGE',on_release=self.dd_lang.open,width=20,height=50)
        self.dd_lang.bind(on_select=lambda instance,x:setattr(self.m_lang,'text',x))
        self.top.add_widget(self.m_lang)
        self.dd_table=DropDown()
        self.tables=['TABLE N. 1','TABLE N. 2','TABLE N. 3','TABLE N. 4','TABLE N. 5']
        for table in self.tables:
            self.b_table=Button(text=table,on_release=lambda b_table:self.dd_table.select(b_table.text),size_hint_y=None,height=50)
            self.dd_table.add_widget((self.b_table))
        self.m_table=Button(text='TABLE N.',on_release=self.dd_table.open,width=50,height=80)
        self.dd_table.bind(on_select=lambda instance,x:setattr(self.m_table,'text',x))
        self.top.add_widget(self.m_table)
        def xit(instance):
            db.close()
            sys.exit()
        self.top.add_widget(Button(background_normal='images/exit.jpeg',width=20,height=50,on_press=xit))
        self.top.add_widget(Label())
        self.hot=BoxLayout()
        self.buttons=BoxLayout(orientation='vertical',size_hint_x=0.3,spacing=50,padding=50)
        self.grid=GridLayout(cols=2,spacing=50,padding=50)
        def dishes(x):
            self.grid.clear_widgets()
            for dish in cdb.execute('select * from '+x).fetchall():
                def add(dish):
                    cdb.execute('insert into cart(nm,prc) values(?,?)',(dish.split(' - ')[0],dish.split(' - ')[1],))
                    db.commit()
                    self.body.clear_widgets()
                    self.datatable.row_data = cdb.execute('select * from cart').fetchall()
                    self.datatable.bind(on_row_press=self.remove)
                    self.body.add_widget(self.datatable)
                    self.tot.text=str('%.2f' %cdb.execute('select sum (prc) from cart').fetchone()[0])
                self.grid.add_widget(Button(text=dish[0]+' - '+dish[2],background_normal=dish[1],
                                            on_press=lambda self:add(self.text),font_size=50,color='black'))
        self.b_first=Button(text='FIRST DISHES',on_press=lambda *args:dishes('first'))
        self.b_second=Button(text='SECOND DISHES',on_press=lambda *args:dishes('second'))
        self.b_side=Button(text='SIDE DISHES',on_press=lambda *args:dishes('side'))
        self.b_fruit=Button(text='FRUIT DISHES',on_press=lambda *args:dishes('fruit'))
        self.b_sweet=Button(text='SWEET DISHES',on_press=lambda *args:dishes('sweet'))
        self.b_drink=Button(text='DRINKS',on_press=lambda *args:dishes('drink'))
        self.buttons.add_widget(self.b_first)
        self.buttons.add_widget(self.b_second)
        self.buttons.add_widget(self.b_side)
        self.buttons.add_widget(self.b_fruit)
        self.buttons.add_widget(self.b_sweet)
        self.buttons.add_widget(self.b_drink)
        def new(instance):
            self.grid.clear_widgets()
            self.t_nm=TextInput(multiline=False,size_hint_y=None,height=50)
            self.t_img=TextInput(multiline=False,size_hint_y=None,height=50)
            self.t_prc=TextInput(multiline=False,size_hint_y=None,height=50)
            self.grid.add_widget(Label(text='DISH: ',color='black',size_hint_y=None,height=50))
            self.dd_dsh = DropDown()
            self.dshs = ['first', 'second', 'side','fruit', 'sweet', 'drink']
            for dsh in self.dshs:
                self.b_dsh = Button(text=dsh, on_release=lambda b_dsh: self.dd_dsh.select(b_dsh.text),size_hint_y=None, height=50)
                self.dd_dsh.add_widget(self.b_dsh)
            self.m_dsh = Button(text='DISH', on_release=self.dd_dsh.open,size_hint_y=None,height=50)
            self.dd_dsh.bind(on_select=lambda instance, x: setattr(self.m_dsh, 'text', x))
            self.grid.add_widget(self.m_dsh)
            self.grid.add_widget(Label(text='NAME: ',color='black',size_hint_y=None,height=50))
            self.grid.add_widget(self.t_nm)
            self.grid.add_widget(Label(text='IMAGE: ',color='black',size_hint_y=None,height=50))
            self.grid.add_widget(self.t_img)
            self.grid.add_widget(Label(text='PRICE: ',color='black',size_hint_y=None,height=50))
            self.grid.add_widget(self.t_prc)
            def doet(instance):
                if self.m_dsh.text=='DISH':
                    dism=Button(text='CLOSE')
                    pop=Popup(content=dism,title='PLEASE SET DISH',size_hint=(None, None), size=(500, 500))
                    dism.bind(on_press=pop.dismiss)
                    pop.open()
                else:
                    cdb.execute('insert into '+self.m_dsh.text+'(nm,img,prc) values (?,?,?)',
                                (self.t_nm.text,'images/'+self.m_dsh.text+'/'+self.t_img.text,self.t_prc.text))
                    db.commit()
                    self.grid.clear_widgets()
            self.grid.add_widget(Button(text='ADD',on_press=doet,size_hint_y=None,height=100))
            def dont(instance):
                self.grid.clear_widgets()
            self.grid.add_widget(Button(text='CLOSE', on_press=dont,size_hint_y=None,height=100))
        self.buttons.add_widget(Button(text='ADD DISH',on_press=new))
        self.cart=BoxLayout(orientation='vertical')
        self.body=BoxLayout(size_hint_y=None,height=800)
        self.cart_buttons=BoxLayout(size_hint_y=None,height=300)
        def bill(instance):
            if self.m_table.text=='TABLE N.':
                dism=Button(text='CLOSE')
                pop=Popup(content=dism,title='PLEASE SET TABLE NUMBER',size_hint=(None, None), size=(500, 500))
                dism.bind(on_press=pop.dismiss)
                pop.open()
                try:self.tot = Label(text=str('%.2f' % cdb.execute('select sum (prc) from cart').fetchone()[0]), color='black')
                except:self.tot = Label(text='0.00', color='black')
            else:
                os.remove('bill')
                file = open('bill', 'a')
                file.write('TL - DaRestaurant - '+datetime.datetime.now().strftime('%d/%m/%Y %H:%M') + ' - '+self.m_table.text+'\n\n')
                for row in cdb.execute('select * from cart').fetchall():
                    file.write(str(row[0])+' - '+row[1]+' - '+row[2]+' $\n')
                file.write('\nTOTAL BILL: '+self.tot.text+' $')
                file.close()
                os.startfile('bill','printer')
                self.tot.text='0.00'
                self.body.clear_widgets()
                cdb.execute('delete from cart')
                db.commit()
                self.datatable.row_data = cdb.execute('select * from cart').fetchall()
                self.datatable.bind(on_row_press=self.remove)
                self.body.add_widget(self.datatable)
                self.grid.clear_widgets()
        self.datatable = MDDataTable(use_pagination=True,column_data=[('ID', dp(30)), ('DISH', dp(30)), ('PRICE', dp(30))],
                    row_data=cdb.execute('select * from cart').fetchall(), sorted_on='DISH',size_hint_y=None,height=950)
        self.datatable.bind(on_row_press=self.remove)
        self.body.add_widget(self.datatable)
        try:self.tot=Label(text=str('%.2f' % cdb.execute('select sum (prc) from cart').fetchone()[0]),color='black')
        except:self.tot=Label(text='0.00',color='black')
        self.cart_buttons.add_widget(Button(text='BILL',background_normal='images/bill.png',on_press=bill,size_hint_x=0.5,size_hint_y=0.7))
        self.cart_buttons.add_widget(Label(text='TOT.: ',color='black'))
        self.cart_buttons.add_widget(self.tot)
        self.cart.add_widget(self.body)
        self.cart.add_widget(self.cart_buttons)
        self.hot.add_widget(self.buttons)
        self.hot.add_widget(self.grid)
        self.hot.add_widget(self.cart)
        self.hot.add_widget(Label(size_hint_x=None,width=50))
        self.page.add_widget(Label(size_hint_y=0.01))
        self.page.add_widget(self.top)
        self.page.add_widget(self.hot)
        return self.page
        runTouchApp(self.b_lang,self.b_table,self.b_dsh)
    def remove(self, instance_table, instance_row):
        cdb.execute('delete from cart where id=?',(instance_row.text,))
        db.commit()
        self.datatable.remove_row(self.datatable.row_data[-1])
        self.datatable.row_data=cdb.execute('select * from cart').fetchall()
        try:self.tot.text = str('%.2f' % cdb.execute('select sum (prc) from cart').fetchone()[0])
        except:self.tot.text = '0.00'
app().run()