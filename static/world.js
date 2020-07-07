var globalData={}
var positive={}
var negative={}
var neutral={}
var dataset
var choice=0
// var date=''

var negativeScale = ['#FFFFFF', '#8B0000']
var neutralScale = ['#FFFFFF', '#00008B']
var positiveScale = ['#FFFFFF', '#006400']
var scale

var text
var val
var minDate
var maxDate

const updateDataforMap = function(date){
  dataset=[globalData[date]['Negative'],globalData[date]['Neutral'],globalData[date]['Positive']]
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(dataset[choice]);
  mapObject.series.regions[0].setScale(scale[choice]);
}

const initializeDataForMap = function(data,date){

  var dates = Object.keys(data)
  var min = new Date(dates[0])
  var max = new Date(dates[dates.length - 1])
  minDate = Math.floor( min.getTime() / 1000 )
  maxDate = Math.floor( max.getTime() / 1000 )

  positive=data[date]['Positive']
  negative=data[date]['Negative']
  neutral=data[date]['Neutral']
  dataset=[negative,neutral,positive]
  text=['Negative Tweets','Neutral Tweets','Positive Tweets']
  scale=[negativeScale,neutralScale,positiveScale]
}

const createMap= function(){

  $('#world-map').vectorMap({
    map: 'world_mill',
    series: {
      regions:[{
        values : dataset[choice],
        scale: scale[choice],
        normalizeFunction: 'polynomial'
      }]
    },
    onRegionTipShow: function(e, el, code){
      el.html(el.html()+' (' + text[choice] + ' - ' + dataset[choice][code] + ')');
    }
  });
}

const chinaPerception = function(data){
  // console.log(data)
  var weeks = Object.keys(data)
  var i;

  for (i = 0; i < weeks.length; i++) {
    let dataset=[]
    var keys = Object.keys(data[weeks[i]])
    keys.map(key => {
      dataset.push(data[weeks[i]][key])
    })
    var basename="pieChart"
    var temp=i+1

    new Chart(document.getElementById(basename.concat(temp.toString())),{
    "type":"polarArea",
    "data":{
      "labels":keys,
      "datasets":[{
        "data":dataset,
        "backgroundColor":["#ff6961","#7EC8E3","#77dd77","rgb(201, 203, 207)"]} //red,blue, green
      ]}
    })
  }
}

// const initiateChart = function(data){
//   var date='2020-03-29'
//   initializeDataForMap(data.world_sentiments,date)
//   createMap()
//   chinaPerception(data.china)
  
//   var sliderObj = document.getElementById("Slider")
//   sliderObj.max=maxDate
//   sliderObj.min=minDate
//   sliderObj.step=86400
//   globalData=data.world_sentiments
//   rangeBullet.innerHTML = temp1;
// }

const initiateChart = function(data){
  var date='2020-03-29'
  initializeDataForMap(data.world_sentiments,date)
  createMap()
  chinaPerception(data.china)
  var rangeBullet = document.getElementById("rs-bullet");
  var sliderObj = document.getElementById("Slider")
  sliderObj.max=maxDate
  sliderObj.min=minDate
  sliderObj.step=86400
  globalData=data.world_sentiments
  console.log(maxDate)
  console.log(minDate)
  let temp=new Date(minDate*1000)
  let temp1=temp.toISOString().substring(0,10)
  console.log(temp1)
  rangeBullet.innerHTML = temp1;

}
$('#positiveTweetButton').on('click',function(){
  choice=2
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(dataset[choice]);
  mapObject.series.regions[0].setScale(scale[choice]);
  // console.log(positive)
})
$('#neutralTweetButton').on('click',function(){
  choice = 1
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(dataset[choice]);
  mapObject.series.regions[0].setScale(scale[choice]);
  // console.log(neutral)
})
$('#negativeTweetButton').on('click',function(){
  choice=0
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(dataset[choice]);
  mapObject.series.regions[0].setScale(scale[choice]);
})

// var slider = document.getElementById("Slider");
// slider.oninput=function(){
//   let temp=new Date(this.value*1000)
//   let temp1=temp.toISOString().substring(0,10)
//   // console.log(temp1)
//   updateDataforMap(temp1)
// }

var rangeSlider = document.getElementById("Slider");
var rangeBullet = document.getElementById("rs-bullet");

var slider = document.getElementById("Slider");
slider.oninput=function(){
  let temp=new Date(this.value*1000)
  let temp1=temp.toISOString().substring(0,10)
  console.log(temp1)
  rangeBullet.innerHTML = temp1;
  updateDataforMap(temp1)
}

const loadData = function(){
  $.ajax({
    url: '/worldData',
    method: "GET",
    success: initiateChart
  })
}

$(function(){
  loadData()
});
