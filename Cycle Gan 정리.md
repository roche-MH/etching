# Cycle Gan 정리

## CycleGAN 으로 할수 있는 일은 무엇인가?

#1 말 <-> 얼룩말 간의 변환이 가능하다

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle0200.jpg)

#2 여름 <-> 겨울 사진 변환도 가능

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle0500.jpg)

#3 아이폰 사진 <-> 아웃오브 포커스 사진 변환가능

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle0100.jpg)

#4 얼굴 <-> 라면과 같은 엽기적인 것도 가능하다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle0700.jpg)

[정리] CycleGAN으로 할수 있는 일

* 사이클 GAN은 사진을 특정 화풍의 그림으로도 바꿀수 있고
* 그림을 사진으로도 바꿀수 있다.
* 같은 맥락의 다른 예제들도 많다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle0800.jpg)

## CycleGAN은 어떻게 동작하는가?

* Cycle GAN을 연구하는 랩실에서 이전에 pix2pix를 만들었다.
* 이부분에 대한 이해를 하고 나면 cycleGAN 이해가 더 와닿는다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle0900.jpg)

그래서 pix2pix -> GAN -> CycleGAN 순으로 정리를 진행한다.

### pix2pix

#1

* 학습
  * supervised learning
  * input, output이 모두 사진
  * 예를 들어 흑백사진 -> 컬러사진
* Test
  * test는 등장한적이 없는 흑백 사진을 주었을때 컬러사진으로 바꾸어야 한다.

#2

* self supervised인 이유는 사람이 label을 굳이 붙여주지 않아도 흑백/컬러 사진을 정답지로 학습시킬 수 있기 때문
* loss 는 |G(x) – y|

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1250.jpg)



#3

* 아래와 같은 트레이닝도 가능하다
  * 입력 : 건물의 구성양식을 픽셀별로 나타낸
  * 정답지 : 실제 건물 사진을 만들어냄

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1100.jpg)

### pix2pix의 한계점 

#1

* pix2pix로 학습을 시켜보면 정답지에 비해 뿌옇고 색깔이 부조화 스러운 현상이 나타남

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1300.jpg)

#2

* 흑백사진 -> 컬러도 마찬가지
* 이런 현상이 발생하는 이유는 loss를 막기 위해 흑백이 아닌 색깔을 모델이 선택을 하는데 이때 색깔값에 대한 가이드라인이 따로 없기 때문에 모델이 중간값을 고르는 경향이 나타남

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1400.jpg)

pix2pix의 intuition

여기서 중요한 intuition은 아래와 같다.

* 사람이 보기에는 output과 Ground Truth의 차이가 명확히 눈에 보인다. 즉 사람은 결과를 구별할 수 있다.
* 사람이 구별할 수 있으면 딥러닝으로도 구별할수 있지 않을까?
* 사람 대신 다른 뉴럴 네트워크가 이 역할을 하게 만들어 보자

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1500.jpg)



## GAN

위 흐름에서 등장한 GAN에 대해 살펴보자

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1600.jpg)



### GAN을 사용하는 목적

* 우리의 목적은 흑백사진 입력을 컬러사진으로 만드는 것이고 이 때 Generator 네트워크를 이용한다.
* Generator를 G라 부른다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle1900.jpg)



GAN 네트워크 구성

* GAN에서는 D를 새로 만들어 G가 real인지 fake인지 구별하게끔 만든다.
* 즉 두 네트워크 미션은 아래와 같다.
  * D는 fake를 구별하려 한다.
  * G는 fake image로 D를 속이려 한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2000.jpg)



GAN 네트워크 수식 정의 : D함수

* D의 입장에서 0에 가까우면 real, 1에 가까우면 fake로 구별한다.
* 그러면 D의 입장에서는 loss 정의는 아래와 같이 할수 있다.
  * logD(G(x))logD(G(x))를 통해 G가 만들어내는 결과는 1(fake)에 가깝게 만든다
  * log(1−D(y))log(1−D(y))를 통해 실제 정답 이미지는 0(real)에 가깝게 만든다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2100.jpg)



GAN 네트워크 수식 정의 : G 함수

마찬가지로 G의 입장에서는 D와 반대로 argMin을 하면 된다.

*  logD(G(x))logD(G(x))를 통해 G가 만들어내는 결과는 0(real)에 가깝게 만든다
* log(1−D(y))log(1−D(y))를 통해 실제 정답 이미지는 1(fake)에 가깝게 만든다



![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2200.jpg)

GAN 네트워크 수식 정의 : 전체 수식

* 수식을 함께 적으면 아래와 같다.
* G입장에서는 D를 가장 잘 속이는 이미지를 만들어 내야 한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2300.jpg)

GAN에 대한 간단한 이해

* G의 관점에는 D가 loss function이다.
* 이를 통해 **G와  D를 경쟁관계로 만드는게 GAN의 장점**이다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2400.jpg)

pix2pix의 Loss 함수

* pix2pix의 loss는 픽셀 level loss와 GAN으로 정의한 loss를 합쳐서 정의함
* 이전보다 성능이 좋아지는게 육안으로 확인됨

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2500.jpg)



## CycleGAN

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2600.jpg)



pix2pix의 또다른 한계점

* pix2pix 처럼 흑백을 컬러사진으로 바꾸는 것은 데이터셋을 구성하기 쉽다.
* 하지만 현실세계에서는 항상 학습을 위한 데이터셋을 구성하기 쉬운게 아니다.



CycleGAN이 하고자 하는것

* 예를 들어 모네의 그림과 실제 사진으로 바꾸는 작업을 학습시킨다고 해보자.
* 완전히 똑같지 않은 원하는 style의 사진을 쉽게 구할수 있다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2700.jpg)

### 기존 GAN Loss를 CycleGAN에서도 사용할수 있을까?

생각해보면 GAN Loss는 동일하게 사용할수 있다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2800.jpg)

### GAN Loss만 사용했을때의 문제점

- 하지만 서로 다른 사진이 같은 target 이미지로 generation 될수 있는 여지를 막을 수 없음
- 즉 아래의 2가지 문제점이 있음
  - Input의 특성이 무시되고
  - 같은 Output으로 매몰될 여지가 있음

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle2900.jpg)

### CycleGAN의 Loss 컨셉

- 핵심 컨셉 : 따라서 추가적인 loss의 조건은 원본 이미지로 reconstruct 되게끔 강제하는 것이다.
- 즉, 이 의미는 사진의 style을 바꾸는데 다시 원래 그림으로 복구가능한 정도로만 바꾸라는 뜻이다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3000.jpg)

### CycleGAN의 Loss 함수

- 기존 GAN Loss는 유지한다.
- 추가적으로 생긴 loss는 가짜이미지를 다시 genration한 이미지와 기존 원본 이미지 x의 loss가 최소화 되어야 한다는 것이다.
- 마치 pix2pix의 pixel level difference를 추가해준 개념이다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3100.jpg)

- 자 따라서 아래의 loss 함수로 위의 역할을 수행할 수 있게 되었다.
- 다음 슬라이드에서 조금만 더 Loss에 대해 생각해보자.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3200.jpg)

### 반대방향 학습

- 같은 맥락으로 반대 방향의 학습도 가능하다. F가 G의 역함수 개념이니까 이게 가능하다.
- 예를들어, 바로 위의 학습이 모네 그림 -> 실사 이미지의 학습이라면 이번에는 실사 이미지 -> 모네 그림으로의 학습을 수행하는 것이다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3300.jpg)

### CycleGAN loss함수의 완성

- 따라서 위의 두 방향의 학습을 합치면 loss가 아래와 같이 된다.
- Cycle GAN은 이 두 방향의 loss를 합친다.
- Cycle GAN 연구Lab에 따르면 실제로 두 방향이 한 방향으로만 학습을 시켜보면 결과가 좋지 않았다고 한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3400.jpg)

### CycleGAN의 학습 결과 #1

- 학습의 결과는 아래와 같다.
- 그림 -> 사진 변환이 가능하다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3500.jpg)

### CycleGAN의 학습 결과 #2

- 반대로 사진 -> 그림으로 바꿀수도 있다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3600.jpg)

### CycleGAN 적용 사례 #1

- loss를 이것저것 뺐을 때 어떤 결과가 있는지 실험을 해보았다. city scape 데이터셋을 살펴보자. 정답지는 사람이 직접 색깔로 label해 놓은 데이터셋이다.
- GAN만 사용하면 input으로 돌아오지 못하고 거의 같은 이미지로 수렴한다.(label 데이터)
- 실험 시 가장 좋은 성능은 CycleGAN을 사용했을때였다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3700.jpg)

### CycleGAN 적용 사례 #2

- 되돌아오는 이미지는 아래와 같다.
- 원본은 GTA 스크린샷, 정답지는 자율주행 차량 사진이다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle3800.jpg)

## CycleGAN 설계 특징

### Generator 아키텍쳐

- Cycle GAN연구에서 G의 아키텍쳐를 세우는게 매우 중요한 것을 발견하였다.
- Disco GAN은 아래와 같은 G 아키텍쳐를 지닌다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4010.jpg)

### CycleGAN의 첫번쨰 아키텍처

- 최초의 Cycle GAN은 U-Net을 사용하였다.
- 장점은 skip connection으로 인해 디테일이 훨씬 더 많이 간직된다는 장점이 있지만
- 단점은 두가지의 컨텐츠가 비슷한 경우 Skip Connecton을 최대한 사용하려고 하여 성능이 좋지 못했다고 한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4020.jpg)

### CycleGAN의 마지막 아키텍처

- ResNet을 사용하였 장점은 이미지 퀄리티 입장에서 좋았는데 단점은 메모리를 많이 사용한다고 한다.
- 학습 파라미터가 적어 많은 변형을 일으킬 수 없다는 특징이 있다

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4040.jpg)

### GAN Loss 함수의 변경

- CycleGAN에서는 cross entropy 사용시 vanishing gradient 문제가 발생했다.
- 따라서 대신에 LSGAN을 사용할 때 성능이 잘 나와서 이를 사용하였다고 한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4100.jpg)

### L1 loss의 필요성

pix2pix에서 확인했듯이 L1 로스를 추가하는것이 성능 향상에 좋은듯 하다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4200.jpg)

### L1 loss의 추가의 어려움

CycleGAN은 아래 이미지를 얼룩말로 바꾸는 정답이 없기 때문에 직접적인 L1 loss를 구하기 어려움

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4300.jpg)

### CycleGAN의 간접적 L1 loss #1

- 얼룩말을 말처럼 바꾼 이미지를 이용하여 가짜 L1 로스(여기서 얼룩말이 정답지)를 넣어서 효과를 보았음
- F(y)로 이미지를 생성한 뒤 이를 G()를 적용하여 정답지 y와 비교

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4400.jpg)

### CycleGAN의 간접적 L1 loss #2

- 당연한 얘기지만 얼룩말을 넣었을때 얼룩말이 나오게끔 나오는 loss를 G에 추가하는 것도 도움이 된다.(identity loss)

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4500.jpg)

### L1 loss를 추가한 결과물

- L1 loss가 더 안정적인 가이드 라인이 되어준다.
- 그림-> 사진 에서 더 안정적인 결과물이 나왔다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4600.jpg)

### Replay Buffer

- GAN 트레이닝을 진행하며 똑같은 샘플별로 성능을 살펴보면 트레이닝을 돌릴때마다 성능이 천차만별이다.
- 이 불안정성을 해결하기 위해 주기적으로 Generator가 만들어놓은 사진을 다시 discriminator에게 보여줌, 이 부분은 Discriminator에게만 적용함

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4700.jpg)

## CycleGAN의 한계점

### 모양

- CycleGAN의 가장 큰 단점은 모양을 바꾸기가 어려움
- 사과를 오렌지로 바꾸는 것도 모양을 바꾸기가 어려움

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4800.jpg)

### 데이터 분포

- 말 위에 사람이 있는 사진이 많지 않을 때 얼룩말로 바꾸는 것이 정상 동작하지 않는다.
- Optimization의 문제라기 보다 Dataset의 문제라고 생각됨

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle4900.jpg)

## Domain Adaption

CycleGAN으로 어떤 도메인에 적용할 수 있는지 사례를 찾아보자.

### GTA5 <-> real streetview

- GTA 사진을 실제 거리뷰로 바꾸는 일을 시켜보았다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5100.jpg)

* 재밌는 점은 정답지에 항상 벤츠 장식이 있어서 이것을 만들어 내는 것을 확일 할 수 있다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5200.jpg)

### GTA와 자율주행의 관계

GTA 이미지 혹은 게임의 의미는 이 게임 자체가 좋은 무인자동차 학습 TOOL이다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5250.jpg)

### GTA를 통한 자율주행 모델링

실사에 가까운 GTA 게임에서 Object Detection을 훈련시키고 실제 도로에서 검증한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5300.jpg)

### GTA를 통한 자율주행 모델링의 한계점

- 하지만 GTA에서 학습된 모델로 실제 환경에서 돌렸을 때 정확도가 그렇게 높지가 않다.
- Per-class accuracy는 object 인식의 확률의 평균(가로등은 몇%, 자동차는 몇% 등)이고 per-pixel accuracy는 픽셀단위 인식의 정확도를 의미한다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5400.jpg)

### 현재 기술의 한계점

현존하는 최고의 기술로 하더라도 6% 향상밖에 안됨

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5450.jpg)

### CycleGAN의 성능 개선

- 별다른 Trick없이 Cycle GAN 으로 이미지를 실사화 하여 훈련시켰을 때 기존의 정확도를 가볍게 뛰어넘었다.
- 이때 per-pixel accuracy로 보더라도 실사 훈련인 93.1% 대비 82.8%로 훌륭하다.

![image-20200525160610298](http://www.kwangsiklee.com/wp-content/uploads/direct/ai/border/cycle5500.jpg)

