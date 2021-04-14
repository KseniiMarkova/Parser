import urllib.request
import csv
from bs4 import BeautifulSoup as bs
import requests as req
import re
import io


def main():
    cleare_files()
    #find_all_urls()
    
    with  io.open("List_URLs.txt", "r", encoding="utf-8") as list_base_url:
        base_list = list_base_url.readlines()
        len_b = file_len()
        for b in range(len_b):
            one_base_url = base_list[b]
            base_url = one_base_url.rsplit('\n')[0]
            course_information(base_url)    
    
def file_len():
    with open('List_URLs.txt') as list_url_len:
        for indx, l in enumerate(list_url_len,1):
            pass
    return(indx)    

#Поиск всех ссылок на странице(исользуется в find_one_url)
def find_all_urls(): 
    
    for i in range(1,101):
        find_URLs_url='https://www.coursera.org/search?query=computer+programming&page='+str(i)+'&index=prod_all_products_term_optimization'
        print('URLs find: ' + str(i))
        find_one_url(find_URLs_url)

#Поиск 10 base_url на 1 странице
def find_one_url(find_URLs_url): 
    resp = req.get(find_URLs_url)
    soup = bs(resp.text, 'lxml')
    with  io.open("URLs.txt", "a", encoding="utf-8") as find_urls:
            find_url = soup.find_all("script", type="application/ld+json")
            rsplit_script_url = str(find_url).rsplit('[<script type="application/ld+json">')[1]
            rsplit_context_url = str(rsplit_script_url).rsplit('{"@context":"http://schema.org","@type":"ItemList","itemListElement":[')[1]
            find_only_url = str(rsplit_context_url).rsplit("]}")[0]
            find_urls.write(str(find_only_url))
    
    with io.open("List_URLs.txt", "a", encoding="utf-8") as list_find_urls:
        for i in range(1,11):
            position_url = '{"@type":"ListItem","position":'+ str(i) +',"url":"'
            rsplit_url = str(find_only_url).rsplit(position_url)[1]
            r_url = str(rsplit_url).rsplit('"}')[0]
            list_find_urls.write(str(r_url)+'\n')

#Поиск информации по курсу
def course_information(base_url):
    resp = req.get(base_url)
    soup = bs(resp.text, 'lxml')
    video = open('videos.txt', 'a')
    min_video = open('min_videos.txt', 'a')
    reading = open('readings.txt', 'a')
    quizzes = open('quizzes.txt', 'a')
    global one_part

    with io.open("front_csv_file.txt", "a", encoding="utf-8") as front_csv:
    #находит название курса
        with  io.open("Title.txt", "a", encoding="utf-8") as title: 
            find_title = soup.find_all("h1", class_= "banner-title m-b-0 banner-title-without--subtitle")        
            len=find_title.__len__()
            if len==1:
                print('Title find')
                split_title = str(find_title).split('>')[1]
                final_title = str(split_title).rsplit('<')[0].replace(';',',')
                title.write(final_title + ';\n')
            else:
                find_title = soup.find_all("h1", class_= "banner-title m-b-0")        
                lens=find_title.__len__()
                if lens==1:
                    print('Title find 2')
                    split_title = str(find_title).split('>')[1]
                    final_title = str(split_title).rsplit('<')[0].replace(';',',')      
                    title.write(final_title + ';\n')
                else:
                    final_title = 'NaN'
                    title.write(final_title + ';\n')                                     
    #находит описание курса  
        with  io.open("Description.txt", "a", encoding="utf-8") as description:   
            find_content_inner = soup.find_all("div", class_= "m-t-1 description")
            len=find_content_inner.__len__()
            if len==0:
                find_content_inner = soup.find_all("div", class_= "m-t-1 m-b-3 description")
                lens = find_content_inner.__len__()
                if lens==1:
                    print('Content inner find class2')
                    content_inners = re.sub(r'<.+?>', '', str(find_content_inner))
                    content_inner = re.sub(r'\n', '',content_inners).split('[')[1].split(']')[0].replace(';',',') 
                    description.write(content_inner+ ';\n')
                else:
                    content_inner = 'NaN'
                    description.write( content_inner + ';\n')
            else:
                print('Content inner find class1')
                content_inners = re.sub(r'<.+?>', '', str(find_content_inner))
                content_inner = re.sub(r'\n', '',content_inners).split('[')[1].split(']')[0].replace(';',',') 
                description.write(content_inner + ';\n')
    #находит информацию по преподавателям   
        with  io.open("InstructorList.txt", "a", encoding="utf-8") as instructor:  
            all_instructors = soup.find_all("h3", class_= "instructor-name headline-3-text bold")
            len=all_instructors.__len__()
            if len==0:
                instructor.write('NaN;')
            else:
                for find_instructor in all_instructors:
                    print('Instructor list find')
                    text_instructors = find_instructor.get_text()
                    instructors = text_instructors.replace(';',',')
                    instructor.write(instructors + ';')
            instructor.write('\n')
    #Число обученных студентов
        with  io.open("students.txt", "a", encoding="utf-8") as students:  
            all_students = soup.find_all("div", class_= "learners-count")
            len=all_students.__len__()
            if len==0:
                students.write('0;')
            else:
                for find_students in all_students:
                    print('Students find')
                    text_students = find_students.get_text()
                    find_students = text_students.replace(';',',').replace('Learners','').replace(' ','')
                    students.write(find_students + ';')
            students.write('\n')
    #Число курсов у преподавателя
        with  io.open("courses_count.txt", "a", encoding="utf-8") as courses_count:  
            all_courses_count = soup.find_all("div", class_= "courses-count")
            len=all_courses_count.__len__()
            if len==0:
                courses_count.write('0;')
            else:
                for find_courses_count in all_courses_count:
                    print('courses_count find')
                    text_courses_count = find_courses_count.get_text()
                    find_all_courses_count = text_courses_count.replace(';',',').replace('Course','').replace('s','').replace(' ','')
                    courses_count.write(find_all_courses_count + ';')
            courses_count.write('\n')
    #находит заголовки учебный план курса
        with  io.open("Syllabus.txt", "a", encoding="utf-8") as syllabus: 
            all_syllabus_title = soup.find_all("h2", class_= "headline-2-text bold m-b-2")
            len = all_syllabus_title.__len__()
            if len==0:
                all_syllabus_title = soup.find_all("h3", class_= "headline-3-text bold m-t-1 m-b-2")
                lens = all_syllabus_title.__len__()
                if lens==0:
                    syllabus.write('NaN;')
                else:
                    for find_syllabus_title in all_syllabus_title:
                        print('Syllabus title find')
                        text_syllabus_title = find_syllabus_title.get_text()
                        syllabus_title = text_syllabus_title.replace(';',',')
                        syllabus.write(syllabus_title + ';')
            else:
                for find_syllabus_title in all_syllabus_title:
                    print('Syllabus title find')
                    text_syllabus_title = find_syllabus_title.get_text()
                    syllabus_title = text_syllabus_title.replace(';',',')
                    syllabus.write(syllabus_title + ';')
            syllabus.write('\n')
    #находит материалы
        with  io.open("Materials.txt", "a", encoding="utf-8") as materials: 
            all_materials = soup.find_all("div", class_= "_wmgtrl9 m-x-1s text-secondary")
            len = all_materials.__len__()
            if len==0:
                materials.write('0;')
                video.write('0;')
                min_video.write('0;') 
                reading.write('0;')
                quizzes.write('0;')
            else:
                for find_material in all_materials:
                    print('Materials find')
                    text_material = find_material.get_text()
                    material = str(text_material.replace('(',',').replace(')',''))
                    materials.write(material + ';')
                    one_part = material
                    check_videos(one_part, video, min_video, reading, quizzes)
            materials.write('\n')
            video.write('\n')
            min_video.write('\n')
            reading.write('\n')
            quizzes.write('\n')
        video.close()
        min_video.close()
        reading.close()
        quizzes.close()
    #находит оценку курса
        with  io.open("rating.txt", "a", encoding="utf-8") as rating: 
            find_rating = soup.find_all("span", class_= "_16ni8zai m-b-0 rating-text number-rating number-rating-expertise")
            len = find_rating.__len__()
            if len==1:
                print('Rating find')
                split_rating = str(find_rating).split('-->')[1]
                final_rating = str(split_rating).rsplit('<!--')[0].replace(';',',')
                rating.write(final_rating + ';\n')
            else:
                find_rating = soup.find_all("span", class_= "_16ni8zai m-b-0 rating-text number-rating m-l-1s m-r-1")
                lens=find_rating.__len__()
                if lens==1:
                    print('Rating find')
                    split_rating = str(find_rating).split('-->')[1]
                    final_rating = str(split_rating).rsplit('<!--')[0].replace(';',',')     
                    rating.write(final_rating + ';\n')
                else:
                    final_rating = '0'
                    rating.write(final_rating + ';\n')      
        #front_csv.write(final_title + ';' + content_inner + ';' + instructor.readlines() + ';' + syllabus.readlines() + ';' + final_rating + ';'+ materials.readlines() + ';\n')

def check_videos(one_part, video, min_video, reading, quizzes):
    videos_par = 'videos'
    video_par = 'video'
    if videos_par in one_part:
        text_videos = one_part.split('videos')[0].replace(' ','').replace(' ','')
        other_text_videos = one_part.split('videos')[1]
        text_min_videos = other_text_videos.split('min')[0].split('Total')[1].replace(' ','')
        other_text_min_videos = one_part.split('min')[1]
        min_video.write(str(text_min_videos)+';')
        video.write(str(text_videos)+ ';')
    elif video_par in one_part:
        text_videos = one_part.split('video')[0].replace(' ','').replace(' ','')
        other_text_videos = one_part.split('video')[1]
        text_min_videos = other_text_videos.split('min')[0].split('Total')[1].replace(' ','')
        other_text_min_videos = one_part.split('min')[1]
        min_video.write(str(text_min_videos)+';')
        video.write(str(text_videos)+ ';')
    else:
        video.write('0;')
        min_video.write('0;')
        other_text_min_videos = one_part
    check_readings(one_part,reading, quizzes, other_text_min_videos)

def check_readings(one_part, reading, quizzes, other_text_min_videos):
    readings_par = 'readings'
    reading_par = 'reading'
    if readings_par in one_part:
        text_readings = other_text_min_videos.split('readings')[0].replace(',','').replace(' ','')
        other_text_readings = other_text_min_videos.split('readings')[1]
        reading.write(text_readings +';')
    elif reading_par in one_part:
        text_readings = other_text_min_videos.split('reading')[0].replace(',','').replace(' ','')
        other_text_readings = other_text_min_videos.split('reading')[1]
        reading.write(text_readings +';')                        
    else:
        reading.write('0;')
        other_text_readings = other_text_min_videos
    check_quizzes(one_part, quizzes, other_text_readings)                    
                
def check_quizzes(one_part, quizzes, other_text_readings):
    quizzes_par = 'quizzes'
    quiz_par = 'quiz'
    if quizzes_par in one_part:
        text_quizzes = other_text_readings.split('quizzes')[0].replace(',','').replace(' ','')
        quizzes.write(text_quizzes + ';')
    elif quiz_par in one_part:
        text_quizzes = other_text_readings.split('quiz')[0].replace(',','').replace(' ','')
        quizzes.write(text_quizzes + ';')
    else:
        quizzes.write('0;')

def cleare_files():
    #with open("List_URLs.txt", "w") as fl:
        #fl.seek(0)
    with open("URLs.txt", "w") as fu:
        fu.seek(0)
    with open("Description.txt", "w") as fd:
        fd.seek(0)
    with open("InstructorList.txt", "w") as fi:
        fi.seek(0)
    with open("rating.txt", "w") as fr:
        fr.seek(0)
    with open("Syllabus.txt", "w") as fs:
        fs.seek(0)
    with open("Title.txt", "w") as ft:
        ft.seek(0)
    with open("front_csv_file.txt", "w") as fcsvf:
        fcsvf.seek(0)
    with open('csv_data.csv', 'w') as fcsv:
        fcsv.seek(0)
    with open('courses_count.txt', 'w') as fcsv:
        fcsv.seek(0)
    with open('students.txt', 'w') as fcsv:
        fcsv.seek(0)
    with open('Materials.txt', 'w') as fcsv:
        fcsv.seek(0)
    with open('videos.txt', 'w') as v:
        v.seek(0)
    with open('min_videos.txt', 'w') as vm:
        vm.seek(0)
    with open('readings.txt', 'w') as r:
        r.seek(0)
    with open('quizzes.txt', 'w') as g:
        g.seek(0)



if __name__ == "__main__":
    main()

