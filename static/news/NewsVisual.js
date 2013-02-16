// Most of the code used here is modified from the Hacker News Visualisation by Marc-Olivier
// https://gist.github.com/ricardmo/4697485
// Many thanks to Marc-Olivier

var newsvis = (function(){

    // Declaring the variables to be used in the visualisation
    var w = 1280,
        h = 500,
        m = 20,
        center = {                                      //gravity center
            x : ( w - m ) / 2,
            y : ( h - m ) / 2
        },
        keyword,              //keyword
        title,               // title for the keyword
        source,             // source of the news
        summary,           //  news sumamry
        timestamp         // news time stamp
        o,               //opacity scale
        r,              //radius scale
        z,             //color scale
        g,            //gravity scale
        t = {         //time factors
             minutes : 1,
             hour    : 60,
             hours   : 60,
             day     : 1440,
             days    : 1440
            },

        gravity  = -0.01,//gravity constants
        damper   = 0.2,
        friction = 0.9,

        // force gravity engine
        force = d3
                .layout
                .force()
                .size([w-m, h-m]),

        // container
        svg = d3
              .select("body")
              .append("svg")
              .attr("width", w + "py")
              .attr("height", h + "px"),

        circles;

    function init(){
        launch();
    }

    function launch() {
        force.
            nodes(???????????);             // defining the node of the forced layout. This node will contain the keyword

        circles = svg
            .append("g")
            .attr("id", "circles")
            .selectAll("a")
            .data(force.nodes());

        // Init all circles at random places on the canvas
        force.nodes().forEach( function(d, i) {
            d.x = Math.random() * w;
            d.y = Math.random() * h;
        });

        var node = circles
            .enter()
            .append("g")
            .append("a")
            .attr("xlink:href", function(d) { return d.url; })
            .append("circle")
            .attr("r", 0)
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
            .attr("fill", function(d) { return z( d.score ); })
            .attr("stroke-width", 2)
            .attr("stroke", function(d) { return d3.rgb(z( d.score )).darker(); })
            .attr("id", function(d) { return "post_#" + d.item_id; })
            .attr("title", function(d) { return d.title; })
            //.style("opacity", function(d) { return o( d.time ); })
            //.on("mouseover", function(d, i) { force.resume(); highlight( d, i, this ); })
            //.on("mouseout", function(d, i) { downlight( d, i, this ); });

        var text = svg.append("svg:g").selectAll("g")
            .data(force.nodes())
            .enter().append("svg:g");

        d3.selectAll("circle")
            .transition()
            .delay(function(d, i) { return i * 10; })
            .duration( 1000 )
            .attr("r", function(d) { return r( d.score ); });

        loadGravity( moveCenter );

        //Loads gravity
        function loadGravity( generator ) {

            force
                .gravity(gravity)
                .friction(friction)
                .charge( function(d) { return g( d.score ); })
                .on("tick", function(e) {
                    generator(e.alpha);
                    node.attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; });

                    //.each(gravity(0.1* e.alpha));
                    //We also want the gravity engine to update text position.
                    text
                        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
                    var q = d3.geom.quadtree(nodes),
                        i = 0,
                        n = nodes.length;
                    while (++i < n){
                        q.visit(collide(nodes[i]));    }

                }).start();

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


    }


})();

