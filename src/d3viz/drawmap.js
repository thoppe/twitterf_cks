
//var MAX_VAL = 0.021*2;
//var MIN_VAL = 0.00;

var cdelta = .03;
var color_center = 0.021;
var MAX_VAL = color_center+cdelta;
var MIN_VAL = color_center-cdelta;

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var colormap = d3.scaleLinear()
    .domain([MIN_VAL, color_center, MAX_VAL])
    .range(["blue", "white", "#a50026"]);

var hexbin = d3.hexbin()
    .extent([[0, 0], [width, height]])
    .radius(14);

var radius = d3.scaleSqrt()
    .domain([0, 12])
    .range([0, 12]);

// Per https://github.com/topojson/us-atlas
var projection = d3.geoAlbersUsa()
    .scale(1280)
    .translate([480, 300]);

var path = d3.geoPath();

d3.queue()
    .defer(d3.json, "https://d3js.org/us-10m.v1.json")
    .defer(d3.tsv, "fucks.tsv", typeWalmart)
    .await(ready);

//.defer(d3.tsv, "walmart.tsv", typeWalmart)

function ready(error, us, walmarts) {
  if (error) throw error;

  svg.append("path")
      .datum(topojson.feature(us, us.objects.nation))
      .attr("class", "nation")
      .attr("d", path);

  svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b)
         { return a !== b; }))
      .attr("class", "states")
      .attr("d", path);

  svg.append("g")
      .attr("class", "hexagon")
    .selectAll("path")
    .data(hexbin(walmarts).sort(function(a, b) { return b.length - a.length; }))
    .enter().append("path")
	.attr("d", function(d) { return hexbin.hexagon(radius(d.length)); })
	.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
	.attr("fill", function(d) {

	    var total = 0, sum = 0;
	    for(i=0;i<d.length;i++)
	    {
		total += d[i]._all;
		sum += d[i].average*d[i]._all;
	    };
	      
	    var wavg = sum/total;
	    wavg = Math.min(wavg, MAX_VAL);
	    wavg = Math.max(wavg, MIN_VAL);

	    var delta = MAX_VAL-MIN_VAL;
	    var c = (wavg - MIN_VAL) / delta;
	   
	    //console.log(c, colormap(wavg));
	    
	    return colormap(wavg);
	});
}

function typeWalmart(d) {
			var p = projection(d);
			d[0] = p[0], d[1] = p[1];
			d.average = +d.average;
			d._all = +d._all;
  return d;
}
