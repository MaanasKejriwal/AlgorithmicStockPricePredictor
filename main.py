import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Insert title here")
st.header("")
st.header("About")
st.text("Insert about here")

st.header("")
st.header("")

a=st.radio("Would you like to know where to invest or understand each Stock?", ("Invest", "Understand"))
if(a=="Invest"):
    st.write("")
    budget=st.sidebar.text_input("Enter your budget: ")
    if(st.sidebar.button("Enter")):
        st.header("")
        st.header("")
        st.write("Here will be the breakdown of where all the person should spend with graphs and shit")

if(a=="Understand"):
    stock_type=st.selectbox("Choose stock",("Apple", "Google", "Samsung"))
    st.sidebar.title("Stock News")
    st.header("")
    st.header("")

    ### News information part starts here

    send="https://www.google.com/search?q=should+you+invest+in+ "+stock_type.lower()+" stock"
    res=requests.get(send)
    soup=BeautifulSoup(res.content, "html.parser")
    all_links=[]
    all_titles=[]
    for i in soup.select("a"):
        link=i.get("href")
        if("/url?q=https://" in link):
            if(("/url?q=https://support.google.com" not in link) and ("/url?q=https://accounts.google.com" not in link)):
                x=link.split("https://")
                y=x[1].split("&sa")
                new="https://"+y[0]
                all_links.append(new)
                z=i.text
                if("..." in z):
                    type2=z.split("...")
                    name=type2[0]
                else:
                    type1=z.split(" › ")
                    name=type1[0]
                all_titles.append(name)
    for i in range(len(all_titles)):
        make="["+str(all_titles[i])+"]"+" "+"("+str(all_links[i])+")"
        st.sidebar.markdown(make)
        st.sidebar.write("")
        st.sidebar.write("")
    
    x_=len(all_titles)
    y_=len(all_links)
    st.write(str(x_))
    st.write(str(y_))


    ##Machine Learning part starts here

    a={}
    c=0
    for i in all_links:
        option=requests.get(i)
        soup=BeautifulSoup(option.content, "html.parser")
        content=[]
        pageinfo=soup.select("p")
        for j in pageinfo:
            content.append(j.text)
        indexnumber=all_links.index(i)
        webname=all_titles[indexnumber]
        a[c]=[webname, content]
        c+=1