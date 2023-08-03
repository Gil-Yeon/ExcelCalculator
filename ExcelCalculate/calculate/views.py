from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def calculate(request):
    file = request.FILES['fileInput']
        # 사용자가 업로드한 파일을 file 변수에 할당
    print('# 사용자가 등록한 파일의 이름: ', file)
    df = pd.read_excel(file, sheet_name='Sheet1', header=0)
        # file을 dataframe형태로 df에 할당
    print(df.head())

    # grade별 value 리스트 만들기
    grade_dic = {}
        # 빈 딕셔너리 생성
    total_row_num = len(df.index)
        # df의 행 수를 저장

    for i in range(total_row_num):
        # df의 행 수 만큼 반복
        data = df.loc[i, :]
            # df의 행을 data에 할당
        if not data.grade in grade_dic.keys():
            # data의 grade 값이 grade_dic의 key값에 없다면 조건문 실행
            grade_dic[data.grade] = [data.value]
                # grade_dic에 key로 data.grade를 value로 data.value를 쌍으로 추가합니다.
        else:
            grade_dic[data.grade].append(data.value)
                # grade_dic의 key값이 data.grade에 value값으로 data.value를 추가한다.
    print(grade_dic)

    grade_calculate_dic = {}
        # 빈 딕셔너리 생성
    for key in grade_dic.keys():
        # grade_dic의 키값들을 불러와 반복
        grade_calculate_dic[key] = {}
            # 각 grade별 빈 딕셔너리 생성
        grade_calculate_dic[key]['min'] = min(grade_dic[key])
            # 각 grade별 최소값    
        grade_calculate_dic[key]['max'] = max(grade_dic[key])
            # 각 grade별 최대값
        grade_calculate_dic[key]['avg'] = float(sum(grade_dic[key])) / len(grade_dic[key])
            # 각 grade별 평균

    print(grade_calculate_dic)

    # 결과 출력
    grade_list = list(grade_calculate_dic.keys())
    grade_list.sort()
    
    for key in grade_list:
        print("# grade: ", key)
        print("min:", grade_calculate_dic[key]['min'], end=" ")
        print("/ max:", grade_calculate_dic[key]['max'], end=" ")
        print("/ avg:", grade_calculate_dic[key]['avg'], end="\n\n")

    # 이메일 주소 도메인별 인원 구하기
    email_domain_dic = {}
    for i in range(total_row_num):
        data = df.loc[i, :]
        email_domain = data['email'].split("@")[1]
            # data의 email값을 @기준으로 분리하여 [1]번째 인덱스 값을 email_domain에 할당
        if not email_domain in email_domain_dic.keys():
            email_domain_dic[email_domain] = 1
                # 도메인이 email_domain_dic에 키값으로 없으면 1 부여
        else:
            email_domain_dic[email_domain] += 1
                # 도메인이 email_domain_dic에 키값으로 존재하면 +1 추가
    
    print('## Email 도메인별 사용 인원')

    for key in email_domain_dic.keys():
        print('#', key, ":", email_domain_dic[key], '명')

    # python과 django에서 pandas는 데이터 타입이 조금 다름
    # pandas의 데이터 타입 --> 파이선 기본 데이터 타입으로 변환

    grade_calculate_dic_to_session = {}
    for key in grade_list:
        grade_calculate_dic_to_session[int(key)] = {}
        grade_calculate_dic_to_session[int(key)]['max'] = int(grade_calculate_dic[key]['max']) # float 자료형으로 변환
        grade_calculate_dic_to_session[int(key)]['avg'] = "{:.6f}".format(float(grade_calculate_dic[key]['avg'])) # float 자료형으로 변환
        grade_calculate_dic_to_session[int(key)]['min'] = int(grade_calculate_dic[key]['min']) # float 자료형으로 변환

    email_domain_dic = dict(sorted(email_domain_dic.items(), key=lambda item:item[1], reverse=True))

    request.session['grade_calculate_dic'] = grade_calculate_dic_to_session
    request.session['email_domain_dic'] = email_domain_dic

    print("")
    print("")
    print("")
    print("")
    print("")
    print(grade_calculate_dic[key])

    return redirect('/result')
        # vewis.result가 아닌 다이렉트로 result페이지로 가야 하므로 name이 아닌 'result' 입력

    # # 위 코드를 간략하게 수정
    # # gropuby 활용
    # grade_df = df.groupby('grade')['value'].agg(['min','max','mean']).reset_index()
    # print(grade_df)
    # print("")
    
    # # pivot_table 활용
    # grade_df_2 = pd.pivot_table(df,
    #                             index = 'grade',
    #                             values = 'value',
    #                             aggfunc = ['min', 'max', 'mean'])
    # grade_df_2.columns = ['min', 'max', 'avg']
    # grade_df_2.reset_index(inplace=True)
    # print(grade_df_2)
    # print("")

    # # groupby 활용
    # df['domain'] = df['email'].str.split('@').str[1]
    # domain_df = df.groupby('domain')['value'].agg('count').sort_values(ascending=False).reset_index()
    # print(domain_df)