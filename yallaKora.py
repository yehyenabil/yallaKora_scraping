import requests
from bs4 import BeautifulSoup  
import csv 


page = requests.get("https://www.yallakora.com/Match-Center/?date=5/28/2023")

def main(page): 
    src = page.content 
    soup= BeautifulSoup(src,"lxml")
    matches_details= []
    
    championships = soup.find_all("div" , {'class': 'matchCard'})
    
    def get_match_info(championships) :
        championship_title = championships.contents[1].find("h2").text.strip()
        all_matches = championships.contents[3].find_all('li')
        nuOfmatches= len(all_matches)
        for i in range (nuOfmatches): 
            #get teams names 
            team_A = all_matches[i].find('div',{'class':'teamA'}).text.strip()
            team_B = all_matches[i].find('div',{'class':'teamB'}).text.strip()
            
            #get score
            match_result = all_matches[i].find('div',{'class':'MResult'}).find_all('span',{'class':'score'})
            score = f" {match_result[0].text.strip()} - {match_result[1].text.strip()}"
            
            #get match time 
            match_time = all_matches[i].find('div',{'class':'MResult'}).find('span',{'class':'time'}).text.strip()
        
            matches_details.append({"champion name":championship_title, "home":team_A,"away":team_B,"time":match_time,"score":score})
        
    for i in range (len(championships)):    
        get_match_info(championships[i])
     
    keys = matches_details[0].keys()   
    
    with open('matchs.csv','w',encoding='utf-8') as output_file :
        dict_writer =csv.DictWriter(output_file ,keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file created")
        
    
main(page)       
    