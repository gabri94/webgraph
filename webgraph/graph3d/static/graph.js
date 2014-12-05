var width = 1200,
    height = 600;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(120)
    .size([width, height]);

var svg = d3.select("#graph-box").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json(island, function(error, graph) {
  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
      .enter().append("line")
      .attr("class", "link")
      .on("mouseover", function(){return tooltip.style("visibility", "visible");})
      .on("mouseenter", function(d){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px"), tooltip.text("Cost: " + (d.weight / 1024));})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
      .style("stroke-width",
        function(d)
        {
          return Math.sqrt(300*d.betweenness+1);
        }
      );

  var node = svg.selectAll(".node")
      .data(graph.nodes)
      .enter().append("circle")
      .attr("class", "node")
      .attr("r", function(d) { return Math.sqrt((d.bw+0.05)*300); })
      .on("mouseover", function(){return tooltip.style("visibility", "visible");})
      .on("mouseenter", function(d){return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px"), tooltip.text("IP: " + d.id);})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
      .call(force.drag);

  var tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden")
      .style("background", "white")
      .style("border-radius", "5px")
      .style("height", "20px")
      .text("");
  //
  // node.append("title")
  //     .text(function(d) { return d.id; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
});
