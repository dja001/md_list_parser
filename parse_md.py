
import os
import glob
import markdown2

#make html list from a number of files containing markdown lists

#read base html/css/javascript file to be updated
html_template_file = 'index_template.html'
with open(html_template_file, 'r') as this_file:
    html_template_content = this_file.read()

#loop over all .md files in todo directory
todo_dir = '/home/dominik/Dropbox/listes/todo/'
print('parsing:')
titled_html=''
for ii, this_file in enumerate(glob.glob(todo_dir+'/*.md')) :
    print(this_file)

    #read markdown content
    with open(this_file, 'r') as md_file:
        md_content = md_file.read()
    
    #convert to html
    bare_html = markdown2.markdown(md_content)
    
    #add nested class to <ul> elements
    ul_html = bare_html.replace('<ul>', '<ul class="nested">')

    #split text content into a python list
    plist_html = ul_html.splitlines()
    for nn, this_line in enumerate(plist_html):
        #add caret class to all list followed by a sub list
        try:
            if plist_html[nn+1][0:3] == '<ul':
                this_line = '<li><span class="caret">'+this_line[4:]+'</span>'
        except:
            pass
        plist_html[nn] = this_line 
        #process items with the #cath hashtag
        if '#cath' in this_line:
            #remove the hashtag
            this_line = this_line.replace('#cath', '')
            #add the cath class to this item
            if 'caret' in plist_html[nn]:
                plist_html[nn] = '<li><span class="caret cath">'+this_line[24:-8]+'</span>'
            else:
                plist_html[nn] = '<li><span class="cath">'+this_line[4:]+'</span>'
    #back to a long string
    classed_html = '\n'.join(plist_html)

    #title of the list is the name of the .md file being procesed 
    file_name = os.path.basename(this_file).split('.')[0]
    titled_html = titled_html + '<li><span class="caret">'+file_name+'</span> \n' + classed_html + '\n</li>'


#insert list in template
html_index_content = html_template_content.replace('__insert_list_here__', titled_html)

#write updates html index
html_index_file = '/home/dominik/Dropbox/listes/todo/index.html'
with open(html_index_file, 'w') as this_file:
    this_file.writelines(html_index_content)

