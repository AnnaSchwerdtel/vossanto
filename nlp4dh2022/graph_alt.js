// based on https://bl.ocks.org/mapio/53fed7d84cd1812d6a6639ed7aa83868

const margin = {top: 5, right: 25, bottom: 20, left: 25};
const width = parseInt(d3.selectAll("#visualization_container").style("width")) - margin.left - margin.right;
const height = parseInt(d3.selectAll("#visualization_container").style("height")) - margin.top - margin.bottom;

var color = d3.scaleOrdinal(d3.schemeCategory10);


d3.json("graph.json").then(function (graph) {
    d3.json("node_infos.json").then(function (node_infos) {
        d3.json("paths.json").then(function (paths) {
            d3.json("image_urls.json").then(function (image_urls) {
                var label = {
                    'nodes': [],
                    'links': []
                };
                var edges = [];

                graph.links.forEach(function (d, i) {
                    edges.push(d.source + d.target)
                })
                console.log(edges)
                console.log(edges.includes("Q41421" + "Q213812"))//[0].source)

                graph.nodes.forEach(function (d, i) {
                    label.nodes.push({node: d});
                    label.nodes.push({node: d});
                    label.links.push({
                        source: i * 2,
                        target: i * 2 + 1
                    });
                });

                var labelLayout = d3.forceSimulation(label.nodes)
                    .force("charge", d3.forceManyBody().strength(-50))
                    .force("link", d3.forceLink(label.links).distance(0).strength(2));

                var graphLayout = d3.forceSimulation(graph.nodes)
                    .force("charge", d3.forceManyBody().strength(-3000))
                    .force("center", d3.forceCenter(width / 2, height / 2))
                    .force("x", d3.forceX(width / 2).strength(1))
                    .force("y", d3.forceY(height / 2).strength(1))
                    .force("link", d3.forceLink(graph.links).id(function (d) {
                        //     console.log(graph)
                        return d.id;
                    }).distance(50).strength(1))
                    .on("tick", ticked);

                var adjlist = [];
                var adjlist2 = [];

                graph.links.forEach(function (d) {
                    adjlist[d.source.index + "-" + d.target.index] = true;
                    adjlist[d.target.index + "-" + d.source.index] = true;
                });

                function neigh(a, b) {
                    return a == b || adjlist[a + "-" + b];
                }

                graph.links.forEach(function (d) {
                    adjlist2[d.source.id + "-" + d.target.id] = true;
                    adjlist2[d.target.id + "-" + d.source.id] = true;
                });

                function neigh2(a, b) {
                    return a == b || adjlist2[a + "-" + b];
                }

                var svg = d3.select("#visualization_container")
                    .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                // .append("g")
                // var svg = d3.select("#viz").attr("width", width).attr("height", height);


                var container = svg.append("g");

                svg.append('defs').append('marker')
                    .attr("id", 'arrowhead')
                    .attr('viewBox', '-0 -5 10 10') //the bound of the SVG viewport for the current SVG fragment. defines a coordinate system 10 wide and 10 high starting on (0,-5)
                    .attr('refX', 23) // x coordinate for the reference point of the marker. If circle is bigger, this need to be bigger.
                    .attr('refY', 0)
                    .attr('orient', 'auto')
                    .attr('markerWidth', 13)
                    .attr('markerHeight', 13)
                    .attr('xoverflow', 'visible')
                    .append('svg:path')
                    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
                    .attr('fill', '#999')
                    .style('stroke', 'none');


                svg.call(
                    d3.zoom()
                        .scaleExtent([.1, 4])
                        .on("zoom", function () {
                            container.attr("transform", d3.event.transform);
                        })
                );

                var link = container.append("g").attr("class", "links")
                    .selectAll("line")
                    .data(graph.links)
                    .enter()
                    .append("line")
                    .attr("stroke", "#aaa")
                    .attr("stroke-width", "1px")
                    .attr('marker-end', 'url(#arrowhead)');

                var node = container.append("g").attr("class", "nodes")
                    .selectAll("g")
                    .data(graph.nodes)
                    .enter()
                    .append("circle")
                    .attr("r", 5)
                // .attr("fill", function(d) { return color(d.group); })

                node.on("click", focus)

                node.call(
                    d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended)
                );

                var labelNode = container.append("g").attr("class", "labelNodes")
                    .selectAll("text")
                    .data(label.nodes)
                    .enter()
                    .append("text")
                    .text(function (d, i) {
                        return i % 2 == 0 ? "" : node_infos[d.node.id]["label"];
                    })
                    .style("fill", "#555")
                    .style("font-family", "Arial")
                    .style("font-size", 12)
                    .style("pointer-events", "none"); // to prevent mouseover/drag capture

                node.on("click", focus);//.on("mouseout", unfocus);

                function ticked() {

                    node.call(updateNode);
                    link.call(updateLink);

                    labelLayout.alphaTarget(0.3).restart();
                    labelNode.each(function (d, i) {
                        if (i % 2 == 0) {
                            // console.log(d.x, d.y)
                            d.x = d.node.x;
                            d.y = d.node.y;
                        } else {
                            var b = this.getBBox();

                            var diffX = d.x - d.node.x;
                            var diffY = d.y - d.node.y;

                            var dist = Math.sqrt(diffX * diffX + diffY * diffY);

                            var shiftX = b.width * (diffX - dist) / (dist * 2);
                            shiftX = Math.max(-b.width, Math.min(0, shiftX));
                            var shiftY = 16;
                            this.setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
                        }
                    });
                    labelNode.call(updateNode);

                }

                function fixna(x) {
                    if (isFinite(x)) return x;
                    return 0;
                }

                function focus(d) {
                    node_id = this.__data__.id
                    node_name = node_infos[node_id]["label"]
                    console.log(node_name)

                    var index = d3.select(d3.event.target).datum().index;
                    node.style("opacity", function (o) {
                        return neigh(index, o.index) ? 1 : 0.3;
                    });
                    // node.style("fill", function (o) {
                    //     return neigh(index, o.index) ? "#34a8eb" : "#555";
                    // })
                    // labelNode.attr("opacity", function (o) {
                    //     return neigh(index, o.node.index) ? 1 : 0.3;
                    // });
                    // link.style("opacity", function (o) {
                    //     return o.source.index == index || o.target.index == index ? 1 : 0.3;
                    // });
                    // link.style("stroke", function (o) {
                    //     return o.source.index == index || o.target.index == index ? "#34a8eb" : "#555";
                    //     ;
                    // });
                    node.style("stroke", "blue");

                    connected = paths[node_id]
                    node.style("fill", function (o) {
                        if (connected[0].includes(o.id) && connected[1].includes(o.id)) {
                            return "#703cd8";
                        } else if (connected[0].includes(o.id)) {
                            return "#EC5552";
                        } else if (connected[1].includes(o.id)) {
                            return "#34eb74";
                        } else {
                            return "#555";
                        }
                    })
                    node.style("opacity", function (o) {
                        // if (neigh(index, o.index)) {
                        //     return 1;
                        // } else
                        if (connected[0].includes(o.id) || connected[1].includes(o.id)) {
                            return 1;
                        } else {
                            return 0.3;
                        }
                    })
                    link.style("opacity", function (o) {
                        if (o.source.index == index || o.target.index == index) {
                            return 1;
                        } else if ((connected[0].includes(o.source.id) && connected[0].includes(o.target.id))
                            || (connected[1].includes(o.source.id) && connected[1].includes(o.target.id))) {
                            return 1;
                        } else {
                            return 0.3;
                        }
                    })
                    link.style("stroke", function (o) {
                        //neighbors
                        if (((edges.includes(o.source.id + o.target.id) && edges.includes(o.target.id + o.source.id))
                                && (o.target.index == index || o.source.index == index))
                            ||
                            //non-neighbors
                            ((edges.includes(o.source.id + o.target.id) && edges.includes(o.target.id + o.source.id))
                                && (connected[0].includes(o.target.id) || connected[1].includes(o.target.id))
                                && (connected[0].includes(o.source.id) || connected[1].includes(o.source.id))
                            )) {
                            return "#703cd8";
                        } else if ((connected[0].includes(o.source.id) && connected[0].includes(o.target.id))
                            || (o.target.index == index)) {
                            return "#EC5552";
                        } else if ((connected[1].includes(o.source.id) && connected[1].includes(o.target.id))
                            || (o.source.index == index)) {
                            return "#34eb74";
                        } else {
                            return "#555";
                        }
                    })

                    // write html in box

                    html_text = ""
                    html_text += "Infos: <br>" +
                        "<a href=https://www.wikidata.org/wiki/" + node_id + ">" + node_name + "</a>"
                    // html_text += "<br><br> Ancestors and Descendants: <br>"

                    // paths[node_id].forEach(function (d) {
                    //     html_text += "<a href=https://www.wikidata.org/wiki/" + d + ">" + d + "</a> <br>"
                    // })
                    html_text += "<br><br> Sentences including " + "<a href=https://www.wikidata.org/wiki/" + node_id + ">" + node_name + "</a> as source: <br>"
                    html_text += "<ul>"
                    console.log(node_id)
                    node_infos[node_id]["VA_src_sents"].forEach(function (d) {
                        splitted = d.split("*")
                        sent = "<li>" + splitted[0] + "<a href=https://www.wikidata.org/wiki/" + node_id + ">" + splitted[1] + "</a>" + splitted[2] + "<br></li>"
                        html_text += sent
                    })
                    html_text += "</ul>"
                    html_text += "<br><br> Sentences including " + "<a href=https://www.wikidata.org/wiki/" + node_id + ">" + node_name + "</a> as target: <br>"
                    html_text += "<ul>"
                    node_infos[node_id]["VA_trg_sents"].forEach(function (d) {
                        splitted = d.split("|")
                        sent = "<li>" + splitted[0] + "<a href=https://www.wikidata.org/wiki/" + node_id + ">" + splitted[1] + "</a>" + splitted[2] + "<br></li>"
                        html_text += sent
                        html_text += "</ul>"
                    });
                    // console.log(html_text)
                    d3.select("#url_p")
                        .html(html_text);


                    // wikidata image by url
                    let image = "";
                    let meta = "";
                    if (image_urls.hasOwnProperty(node_id)) {
                        image += "<a href='https://commons.wikimedia.org/wiki/File:" + image_urls[node_id]["sourceImId"] + "'>" +
                            "<img src='https://upload.wikimedia.org/wikipedia/commons/" + image_urls[node_id]["sourceImThumb"] + "'/></a><br>";
                        meta += "image: <a href='https://commons.wikimedia.org/wiki/File:" + image_urls[node_id]["sourceImId"] + "'>Wikimedia Commons</a>";
                        // if (e.sImLi) image += ", license: " + e.sImLi;

                        meta += ", license:  " + image_urls[node_id]["permissions"]
                        d3.select("#image_container")
                            .html(image + meta);
                    } else {
                        d3.select("#image_container")
                            .html("No image available.");
                    }


                }

                function unfocus() {
                    labelNode.attr("opacity", 1);
                    node.style("opacity", 1);
                    link.style("opacity", 1);
                }

                function updateLink(link) {
                    link.attr("x1", function (d) {
                        return fixna(d.source.x);
                    })
                        .attr("y1", function (d) {
                            return fixna(d.source.y);
                        })
                        .attr("x2", function (d) {
                            return fixna(d.target.x);
                        })
                        .attr("y2", function (d) {
                            return fixna(d.target.y);
                        });
                }

                function updateNode(node) {
                    node.attr("transform", function (d) {
                        return "translate(" + fixna(d.x) + "," + fixna(d.y) + ")";
                    });
                }

                function dragstarted(d) {
                    d3.event.sourceEvent.stopPropagation();
                    if (!d3.event.active) graphLayout.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }

                function dragged(d) {
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                }

                function dragended(d) {
                    if (!d3.event.active) graphLayout.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }
            })
        })
    })
})
;