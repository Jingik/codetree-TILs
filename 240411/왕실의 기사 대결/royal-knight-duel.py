di =[-1,0,1,0 ] #상,우,하,좌
dj =[0,1,0,-1]

L,N,Q = map(int,input().split())
arr=[[2]*(L+2)] + [[2]+list(map(int,input().split()))+[2] for _ in range(L)]+ [[2]*(L+2)]
units = {} # 새로운 입력 저장용 / # 1:r,c,w,h,k 2:r,c,w,h,k 
init_k = {} # 초기 체력 저장용 / # 1:k , 2:k 

for i in range(1,N+1): # 이렇게 해야 units 인덱스 시작 1로 가능 
    si,sj,h,w,k = map(int,input().split())
    units[i]= [si,sj,h,w,k]
    init_k[i] = [k] # 초기 체력 저장용

def push_unit(idx,dr,arr,units,di,dj):
    q=[]     #밀 대상들       # push 후보를 저장
    pset=[]        # 이동 기사번호 저장(중복체크 위함)
    damage=[0]*(N+1)     # 각 유닛별 데미지 누적 
    q.append(idx)      # 초기데이터 append
    pset.append(idx)

    while q:# q에 데이터가 있는 동안 
        cur=q.pop(0)     # 첫번째 요소 제거  # q에서 데이터 한개 꺼냄 #기사 번호  # q: 선입선출 FIFO 이므로 # q.pop()은 끝에 요소 제거 
                        # 근데 돌려보니 또 상관 없긴함 
        ci,cj,h,w,k= units[cur] # 기사 위치 가져오기 #cur 0,1,2,3 순 

        ni,nj= ci+di[dr], cj+dj[dr]# 명령받은 방향진행, 벽이아니면, 겹치는 다른조각이면 => 큐에 삽입
        for i in range(ni, ni+h):       # 벽!! => 모두 취소
            for j in range(nj,nj+w):       # 벽이면 밀수 없으니 그냥 끝내. 
                if arr[i][j]==2: # 벽이라면 
                    return     
                elif arr[i][j]==1: # 함정이라면 
                    damage[cur]+=1   # 데미지 누적 
        # 움직였을 때 다른 유닛이 있으면 계도 움직여야 하니 
        # 겹치는 다른 유닛있는 경우 큐에 추가(모든 유닛 체크)
        for i in units:
            if i in pset: continue # 이미 움직일 대상이면 체크할 필요없음
            ti,tj,th,tw,tk= units[i]  

            if ni<=ti+th-1 and ni+h-1>=ti and tj<=nj+w-1 and nj<=tj+tw-1: # 겹치는 경우
                q.append(i)
                pset.append(i)     

    # 명령 받은 기사는 데미지 입지 않음
    damage[idx]=0 # 다시 0으로 맞추기 

    # 이동, 데미지가 체력이상이면 삭제처리
    for idx in pset:
        si,sj,h,w,k = units[idx]

        if k<=damage[idx]:  # 체력보다 더 큰 데미지면 삭제
            units.pop(idx)
        else:
            ni,nj=si+di[dr], sj+dj[dr]
            units[idx]=[ni,nj,h,w,k-damage[idx]]






for _ in range(Q):
    idx,dr = map(int,input().split())
    if idx in units:
        push_unit(idx,dr,arr,units,di,dj)

answer=0
for idx in units:
    answer += init_k[idx][0] - units[idx][4] # 이런 생각하기가 쉽지가 않군 
    
print(answer)