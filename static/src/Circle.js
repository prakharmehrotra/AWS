var w = 1280,
    h = 500,
    m = 20,
    center = {                                      //gravity center
        x : ( w - m ) / 2,
        y : ( h - m ) / 2
    },
    fill = d3.scale.category20(),
    nodes = d3.range(20).map(function() { return {radius: Math.random() * 60 + 10}; }); // sets the number of nodes (circles in this case)

var gravity = 0.05,
    damper = 0.02;

// creating a container vis
var vis = d3.select("body").append("svg:svg")
    .attr("width", w)
    .attr("height", h);

// starting the gravity engine
var force = d3.layout.force()
    .nodes(nodes)
    .links([])
    .size([w, h])
    .start();

// defining a variable 'node' which will be later used
var node = vis.selectAll("circle.node")
    .data(nodes)
    .enter().append("svg:circle")
    .attr("class", "node")
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .attr("r", function(d) { return d.radius; })
    .style("fill", function(d, i) { return fill(i & 3); })
    .style("stroke", function(d, i) { return d3.rgb(fill(i & 3)).darker(2); })
    .style("stroke-width", 1.5)
    //.on("mouseover", function(){d3.select(this).style("fill", "aliceblue");})
    //.on("mouseout", function(){d3.select(this).style("fill", "green");})
    .call(force.drag);

// defining properties of container
vis.style("opacity", 1e-6)
    .transition()
    .duration(10)
    .style("opacity", 1);

//binding text
var text = vis.append("svg:g").selectAll("g")
    .data(force.nodes())
    .enter().append("svg:g");

text.append("svg:text")
    .attr("x", 8)
    .attr("y", ".31em")
    .attr("text-anchor", "middle")
    .text(function(d) { return 'Shota Puppy'; });


loadGravity( moveCenter );

//Loads gravity
function loadGravity( generator ) {

    force
        .gravity(gravity)
        //.charge(function(d, i) {return i &1; })
        .on("tick", function(e) {

        // Push different nodes in different directions for clustering.
        var kx = 7* e.alpha;
        var ky = 7* e.alpha;
        nodes.forEach(function(o, i) {
            o.y += i & 1 ? ky : -ky;
            o.x += i & 2 ? kx : -kx;
            var q = d3.geom.quadtree(nodes),
                i = 0,
                n = nodes.length;
            while (++i < n){
                q.visit(collide(nodes[i]));    }
        });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
        //.each(gravity(0.1* e.alpha));
        //We also want the gravity engine to update text position.
        text
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });

}

// Generates a gravitational point in the middle
function moveCenter( alpha ) {
    force.nodes().forEach(function(d) {
        d.x = d.x + (center.x - d.x) * (damper + 0.02)*alpha;
        d.y = d.y + (center.y - d.y) * (damper + 0.02)*alpha;
    });
}



//collision detection
function collide(node) {
    var jitter = 0.5;
    var r = node.radius + 16;
        nx1 = node.x - r,
        nx2 = node.x + r,
        ny1 = node.y - r,
        ny2 = node.y + r;
    return function(quad, x1, y1, x2, y2) {
        if (quad.point && (quad.point !== node)) {
            var x = node.x - quad.point.x,
                y = node.y - quad.point.y,
                l = Math.sqrt(x * x + y * y),
                r = node.radius + quad.point.radius;
            if (l < r) {
                l = (l - r) / l * jitter;
                node.x -= x *= l;
                node.y -= y *= l;
                quad.point.x += x;
                quad.point.y += y;
            }
        }
        return x1 > nx2
            || x2 < nx1
            || y1 > ny2
            || y2 < ny1;
    };
}
// click functionality
d3.select("body").on("click", function() {
    nodes.forEach(function(o, i) {
        o.x += (Math.random() - .5) * 40;
        o.y += (Math.random() - .5) * 40;
    });
    force.resume();
});





/*dataset = ['Hi', 'Bye', 'Hello', 'Zero']

var circledata = [];

/*var circledata = [
        { "cx": xx, "cy": yy, "radius": rad, "color" : "green" , "data1": dataset[0]},
        { "cx": xx+200, "cy": xx, "radius": rad, "color" : "purple", "data1": dataset[1] }];

for (i = 0; i<4; i++){

    xx = Math.random()*200+100*i;
    yy = Math.random()*150+100*i;
    rad = Math.random()*100+10*i;
    circledata.push({"cx": xx, "cy": yy, "radius": rad, "color" : "green" , "data1": dataset[i]});
}

w = 960;
h = 600;
m = 20;

// gravity engine parameters
gravity  = -0.01,//gravity constants
damper   = 0.2,
friction = 0.9;

// gravity engine
var force = d3
    .layout
    .force()
    .size([w-m, h-m])
    .nodes(node)
    .start();

// Defining Container
var svg = d3.select("body")
    .append("svg")
    .attr("width", w+"px")
    .attr("height", h+"px");

var circles = svg.selectAll("circle")
    .data(circledata)
    .enter()
    .append("circle");

var circleAttributes = circles
    .attr("cx", function(d) {return d.cx;})
    .attr("cy", function(d) {return d.cy;})
    .attr("r",function(d) {return d.radius;} )
    .attr("fill",function(d) {return d.color;} )
    .style("stroke", "black")
    .on("mouseover", function(){d3.select(this).style("fill", "aliceblue");})
    .on("mouseout", function(){d3.select(this).style("fill", "green");});


var circleText = svg.selectAll("text")
    .data(circledata)
    .enter()
    .append("text");

var textAttributes = circleText
    .attr("x", function(d){ return d.cx;})
    .attr("y", function(d){ return d.cy;})
    .attr("text-anchor", "middle")
    .text(function(d) { return d.data1; });

var nodes = circles


loadGravity(moveCenter);

function loadGravity(generator) {
    force
        .gravity(gravity)
        .charge(-30)
        .friction(friction)
        .on("tick", function(e) {
            generator(e.alpha);
            node
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });

            //We also want the gravity engine to update text position.
            text
                .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        }).start();
}

// Generates a gravitational point in the middle
function moveCenter( alpha ) {
    force.nodes().forEach(function(d) {
        d.x = d.x + (center.x - d.x) * (damper + 0.02) * alpha;
        d.y = d.y + (center.y - d.y) * (damper + 0.02) * alpha;
    });

}*/




