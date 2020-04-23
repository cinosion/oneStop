// 読み込み -> 変換 -> 加工(削落 -> 時間) -> 評価(時間 -> 並替(リスト)) -> 加工(HTML) -> document -> yey
//カード整形 -> 一行だけ試す -> 全部試す -> つくる人更新日時カード -> cron -> git -> yey

// top
// clife
// bun
// socinfo
// corona
// infocial

/*
<div class="column-content card">
<a class="card-link" href="https://www.chuo-u.ac.jp/academics/faculties/letters/major/french/news/2020/04/49016/">
</a>
<p class="card-date card-text today/before">4/<strong>17</strong> 14:30</p><p class="card-category card-text">カテゴリ</p>
<p class="card-title card-text">【重要】遠隔授業への対応のお願い</p>
</div>
*/



//// bridge.jsの読み込み
try{cplusList=cplusFromBridge} catch(e){}
try{topList=topFromBridge} catch(e){}
try{clifeList=clifeFromBridge} catch(e){}
try{bunList=bunFromBridge} catch(e){}
try{socinfoList=socinfoFromBridge} catch(e){}
try{coronaList=coronaFromBridge} catch(e){}
try{infocialList=infocialFromBridge} catch(e){}



//// 処理して追加
function createCardElement(channelName){
  let cardsList = eval(`${channelName}List`)
    for(cardDict of cardsList){
      let title = cardDict['title']
      let date = new Date(cardDict['strfDate'])
      let link = cardDict['link']
      let category = cardDict['category']
      // try{category = cardDict['category'];} catch(e){category = ''}
      let period = 'today'
      let nowDate = new Date();
      if(nowDate.getTime()-date.getTime() > 1000*60*60*(24+12)){
        period = 'before'
      }
      let spanCategory = ''
      if(category != 'null'){
        spanCategory = `<span class="card-category card-text">${category}</span></p>`
      }
let cardXml = `<div class="column-content card">
<a class="card-link" href="${link}"></a>
<p calss="card-text"><span class="card-date card-text ${period}">${date.getMonth()}/<strong>${date.getDate()}</strong> ${date.getHours()}:${date.getMinutes()}</span>${spanCategory}
<p class="card-title card-text">${title}</p>
</div>`
      let scroll =  document.getElementById(`${channelName}Scroll`);
      scroll.insertAdjacentHTML('beforeend', cardXml);
    }
}



//// メインの処理呼び出し
createCardElement('cplus');
createCardElement('top');
createCardElement('clife');
createCardElement('bun');
createCardElement('socinfo');
createCardElement('corona');
createCardElement('infocial');



//// 更新日時の関数
function createRenewalElement(){
  try{exeTime=executeTime} catch(e){}
  let date = new Date(exeTime)
  let dateNow = new Date();
  let period = 'today'
  if(dateNow.getTime()-date.getTime() > 1000*60*60*(24)){
    period = 'before'
  }
let cardXml = `<div class="column-content card">
<a class="card-link" href="#"></a>
<p calss="card-text"><span class="card-date card-text ${period}">${dateNow.getMonth()}/<strong>${dateNow.getDate()}</strong> ${dateNow.getHours()}:${dateNow.getMinutes()}</span></p>
<p class="card-title card-text">最終更新日時</p>
</div>`
  let scroll =  document.getElementById(`subScroll`);
  scroll.insertAdjacentHTML('afterbegin', cardXml);
}



//// 更新日時の呼び出し
createRenewalElement()
































