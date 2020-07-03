var globalData={}
var positive={}
var negative={}
var neutral={}
var dataset
var choice=0
var date=''
var negativeScale = ['#FFFFFF', '#8B0000']
var neutralScale = ['#FFFFFF', '#00008B']
var positiveScale = ['#FFFFFF', '#006400']
var text
var val
var minDate
var maxDate


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
}

const createMap= function(){
  var dataValues
  var scaleValue

  $('#world-map').vectorMap({
    map: 'world_mill',
    series: {
      regions:[{
        values : negative,
        scale: negativeScale,
        normalizeFunction: 'polynomial'
      }]
    },
    onRegionTipShow: function(e, el, code){
      el.html(el.html()+' (' + text[choice] + ' - ' + dataset[choice][code] + ')');
    }
  });
}

const chinaPerception = function(data){
  console.log(data)
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
        "backgroundColor":["#ff6961","#7EC8E3","#77dd77","rgb(201, 203, 207)"]}
      ]}
    })
  }
}

const initiateChart = function(data){
  date='2020-03-29'
  initializeDataForMap(data.world_sentiments,date)
  console.log(negative)
  createMap()
  console.log(data)
  chinaPerception(data.china)

}

$('#positiveTweetButton').on('click',function(){
  choice=2
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(positive);
  mapObject.series.regions[0].setScale(positiveScale);
  // console.log(positive)
})
$('#neutralTweetButton').on('click',function(){
  choice = 1
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(neutral);
  mapObject.series.regions[0].setScale(neutralScale);
  // console.log(neutral)
})
$('#negativeTweetButton').on('click',function(){
  choice=0
  var mapObject = $('#world-map').vectorMap('get', 'mapObject');
  mapObject.series.regions[0].setValues(negative);
  mapObject.series.regions[0].setScale(negativeScale);
  // console.log(negative)
})

// $('#Slider').slider({
//   value : val,
//   min: minDate,
//   max: maxDate,
//   step: 86400,
//   slide: function(event, ui){
//     val = ui.value
//     var mapObject = $('#world-map').vectorMap('get', 'mapObject')
//     var d = new Date(val)
//     console.log(d)
//   }
// })

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
