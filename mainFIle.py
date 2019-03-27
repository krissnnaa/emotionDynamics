import json
import requests
import re
import nltk
from gensim.models import Word2Vec

login_number = 0

commentCollection=[]
def load_issues( url=None, owner_name=None, repo_name=None, dest_path=None, authentication=None):
    i = 0
    global login_number
    global commentCollection

    output_list = []

    params = {'state': 'all'}
    while True:
        print(i)
        if url is None:
            url = "https://api.github.com/repos/" + owner_name + "/" + repo_name + "/pulls"
        url_a = url + '?page={0}'.format(i)
        r = requests.get(url_a, params,
                         auth=(authentication[login_number]['username'], authentication[login_number]['password']))

        if not r.json():
            break
        else:
            if r.status_code == 200:
                print("Yeah successful")
                issueRequest = r.json()
                output_list.append(issueRequest)
                # json.dump(issueRequest, infile)
                i += 1
            else:
                error = r.json()
                print(repo_name + '\t has an error message:\n' + error['message'])
                if r.status_code == 403:
                    print(r.status_code)
                    if login_number < 18:
                        login_number = login_number + 1
                    else:
                        login_number = 0
                    while True:
                        r = requests.get(url_a, auth=(
                            authentication[login_number]['username'], authentication[login_number]['password']))
                        if r.status_code == 200:
                            print("Yeah Successful")
                            pullrequest = r.json()
                            output_list.append(issueRequest)
                            # json.dump(pullrequest, infile)
                            i += 1
                            break
                else:
                    break

    commentCollection.append(output_list)
    if repo_name is not None:
        with open(dest_path + "/" + repo_name + ".json", "w") as infile:
            json.dump(output_list, infile)

if __name__=='__main__':

    with open("authentication.json") as outfile:
        authentication = json.load(outfile)

    dest_path = "/home/krishna/PycharmProjects/CommitCollection/pullFolder/"
    readingPull=0
    if readingPull==1:
        project_={'ipython':'ipython'}

        for key,value in project_.items():
            load_issues(None,key, value, dest_path, authentication)

    with open(dest_path+"ipython.json") as f:
        file=json.load(f)

    commentLinks=[]

    for itemList in  file:
        for index in range(len(itemList)):
            createdDate=re.findall(r'^\d+',itemList[index]['created_at'])
            if int(createdDate[0])<2018:
                continue
            else:

                commentLinks.append(itemList[index]['_links']['review_comments']['href'])

    with open(dest_path + "commentsFrom2018.txt",'w') as f:
        f.write(str(commentLinks))

    if readingPull==1:
        for item in commentLinks:
            load_issues(item,None,None,dest_path,authentication)

        with open(dest_path + "/" + "commentsCollection" + ".json", "w") as f:
            json.dump(commentCollection, f)

        with open(dest_path+"commentsCollection.json") as f:
            file=json.load(f)

        file = [x for x in file if len(x) > 0]

        memberComment={}
        for itemList in file:
            for insideItem in itemList:
                for index in range(len(insideItem)):
                    authorAssociation = insideItem[index]['author_association']
                    memberName=insideItem[index]['user']['login']
                    commentBody=insideItem[index]['body'] + ' '
                    flag=0
                    initialComment=[]
                    if authorAssociation == 'MEMBER':
                        for key,value in memberComment.items():
                            if key == memberName:
                                previousComment=memberComment[memberName]
                                previousComment.append(commentBody)
                                memberComment[key]=previousComment
                                flag=1
                                break

                        if flag==0:
                            initialComment.append(commentBody)
                            memberComment[memberName] = initialComment

        with open(dest_path + "individualComments.json",'w') as f:
            json.dump(memberComment,f)

    with open(dest_path + "individualComments.json") as f:
        file = json.load(f)

    preProcessComments={}
    for key,value in file.items():
        joinedValue=' '.join(value)
        valueString=(re.sub(r'[^\w\s]', '', joinedValue)).lower()
        tokenWords=nltk.tokenize.word_tokenize(valueString)
        preProcessComments[key]=tokenWords
        model = Word2Vec([tokenWords], window=6, size=310,negative=5, min_count=1)
        model.wv.save_word2vec_format(dest_path+key+'.txt', binary=False)
  
