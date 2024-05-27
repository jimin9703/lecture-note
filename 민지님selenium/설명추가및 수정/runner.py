import os
import time
import pandas as pd
from helpers.crawlingsele import User


if __name__ =='__main__':
    user = User()
    user.getBrowser('https://www.danawa.com/',new_window=True)
    user.search_keword('//*[@id="AKCSearch"]', '맥북')
    user.click_button('//*[@id="srchFRM_TOP"]/fieldset/div[1]/button') # 검색버튼
    user.scroll_down() # 내려서
    # user.click_button('//*[@id="SearchOption_Brand_Rep"]/div[1]/div/label/span[1]') 상세검색 체크박스 --> 생략
    user.scroll_down(200)
    # user.click_button('//*[@id="opinionDESC"]')  # 상품평 많은 순 --> 생략
    time.sleep(3)
    user.click_button('/html/body/div[2]/div[4]/div[3]/div[2]/div[8]/div[1]/div[2]/div[3]/ul/li[1]/div/div[2]/p/a')  # 상품이름 클릭
    
    time.sleep(3)
    user.change_window() # 탭 전환
    user.scroll_down(600, init_pos=True)
    user.click_button('//*[@id="bookmark_cm_opinion_item"]/a/h3') # 의견/리뷰 누르기
    user.click_button('//*[@id="danawa-prodBlog-productOpinion-button-tab-companyReview"]') # 쇼핑몰 상품 리뷰 클릭
    time.sleep(3)
    user.scroll_down(300)

    rev_lst = []
    star_lst = []
    for i in range(6):
        try:
            for j in range(10): # 제목이나 사이트 등 더 추가하고 싶다면 여기서 추가 입력
                txt = f'/html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/ul/li[{j+1}]/div[2]/div/div[2]' # 본문
                star = f'/html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/ul/li[{j+1}]/div[1]/span[1]/span' # 별점
                txt = user.find_ele_text(txt)
                print(txt)
                star = user.find_ele_text(star)
                print(star)
                rev_lst.append(txt)
                star_lst.append(star)

        except :
            break

        if i == 5:
            user.click_button('/html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/span')

        else :
            print(f'------------ {i+1}번 finished!! -------------')
            time.sleep(2)
            user.click_button(f'/html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/a[{i+1}]')
            
            ## 오류가 났던 이유
            # 나머지 페이지들의  PATH : /html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/a[1] # page 1
            # 마지막 페이지(6쪽) PATH : /html/body/div[2]/div[5]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[3]/div[2]/div[5]/div/div/div/span
            time.sleep(5)    
        
    user.close_connect()
    print(f'리뷰 {len(rev_lst)}개, 별점 {len(star_lst)}개가 저장되었습니다.')

    df = pd.DataFrame({'리뷰':rev_lst, '별점':star_lst})
    # result 파일 경로 만들기
    result_path = os.path.join(os.getcwd(),'result')
    os.makedirs(result_path, exist_ok=True)
    # csv로 저장
    df.to_csv(os.path.join(result_path,'review.csv'), index=False, encoding='utf-8')
    print(f'#### "review.csv"가 {result_path}에 저장되었습니다. ####')