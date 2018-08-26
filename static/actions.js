var currentId=1;
var source="";
var target="";
var edges = [];
var nodes = [];

$( document ).ready(function() {
  $(document).one('click', function() {
    insertShape('circle');
  });

  $(document).on("dblclick",".shape",function (e) {
    console.log($(this).attr('id'));
    var text = prompt("Enter text", "x=0");
    console.log(text);
    $(this).text(text);
  });

  $(document).on("click",".shape",function (e) {
    if(e.altKey && e.shiftKey){
      jsPlumb.remove($(this).attr('id'));
    }

    if (e.shiftKey && !e.altKey) {
        source = $(this).attr('id');
        console.log("Source: "+source);
        addArrow();
    }
    if (e.altKey && !e.shiftKey) {
        target = $(this).attr('id');
        console.log("Target: "+target);
        addArrow();
    } 
  });
});

function sendGraphCPP(){
  $.post("cpp", JSON.stringify(edges), function(){});
}

function endpointsInfo(){
  edges=[];
  nodes=[];
  const set = new Set();
  for(x in jsPlumb.getConnections()){
    item = {};
    node_item = {};
    item['source'] = jsPlumb.getConnections()[x].sourceId;
    item['target'] = jsPlumb.getConnections()[x].targetId;
    item['label'] = jsPlumb.getConnections()[x]._jsPlumb.overlays.label.label;
    edges.push(item);

    if(!set.has(item['source'])){
      node_item[item['source']] = $('#'+item['source']).text();
      set.add(item['source']);
      nodes.push(node_item);
      node_item={};
    }
    if(!set.has(item['target'])){
      node_item[item['target']] = $('#'+item['target']).text();
      set.add(item['target']);
      nodes.push(node_item);
      node_item={};
    }
  }
  console.log(edges);
  console.log(nodes);
}

function addArrow(){
  var label = "";
  var sourceAnchor="Bottom";
  var targetAnchor="Top";
  if(source!="" && target!=""){
    if($('#'+source).hasClass('diamond')){
      label = prompt("Label", "Yes/No");
      if(label=="No"){
        sourceAnchor="Right";
      }
    }
    jsPlumb.ready(function() {
      var common = {
        connector: ["Straight"],
        anchor: [sourceAnchor, targetAnchor],
        endpoint:"Dot"
      };

      jsPlumb.connect({
          source: source,
          target: target,
          endpoint:"Rectangle",
          overlays:[ 
              ["Arrow" , { width:12, length:12, location:0.67 }],
              [ "Label", {label:label, id:"label"}]
          ]
      }, common);
      target="";
      source="";
    });
  }
}

function readText(){
  console.log($(this));
  var text = prompt("Enter text", "x=0");
  console.log(text);
  $('#newid1').innerHTML = text;
}

function insertShape(geo_form){
  var shape = $('#mydiv').clone();
  newid="newid"+currentId.toString();
  currentId++;
  shape.attr('id', newid)
  shape.addClass("shape");
  shape.addClass(geo_form);
  shape.appendTo(document.body);
  jsPlumb.draggable(newid);

  var endpointOptions = {isSource:true};
  var endpoint = jsPlumb.addEndpoint(newid, endpointOptions);
  endpointOptions = {isTarget:true, endpoint:"Rectangle", paintStyle:{fill:"gray"}};
  endpoint =jsPlumb.addEndpoint(newid, endpointOptions);
}

