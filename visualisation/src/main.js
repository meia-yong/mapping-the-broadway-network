import Graph from "graphology";
import Sigma from "sigma";
import Papa from "papaparse";


const graph = new Graph();


const DATA_FILE = "/data/drl_linear_1_15.csv";
const EDGE_FILE = "/data/performer_edges_clean.csv";


let selectedNode = null;

let highlightedNodes = new Set();

let highlightedEdges = new Set();

let collaboratorsOnly = false;



Papa.parse(DATA_FILE, {

    download: true,
    header: true,


    complete: (nodeResults) => {


        console.log(
            "Loaded nodes:",
            nodeResults.data.length
        );



        // -----------------------
        // Load nodes
        // -----------------------

        nodeResults.data.forEach((row) => {


            graph.addNode(
                row.id,
                {

                    x: Number(row.x),

                    y: Number(row.y),

                    size: Number(row.size),

                    label:
                        row.performer_name,

                    color:
                        "rgba(120,120,120,0.7)"

                }
            );


        });





        // -----------------------
        // Load edges
        // -----------------------

        Papa.parse(EDGE_FILE, {

            download: true,
            header: true,


            complete: (edgeResults) => {



                console.log(
                    "Loaded edges:",
                    edgeResults.data.length
                );



                let skippedEdges = 0;



                edgeResults.data.forEach((row) => {



                    if (
                        !row.source ||
                        !row.target ||
                        !graph.hasNode(row.source) ||
                        !graph.hasNode(row.target)
                    ) {

                        skippedEdges++;

                        return;

                    }



                    graph.addEdge(
                        row.source,
                        row.target,
                        {

                            weight:
                                Number(row.weight)

                        }
                    );


                });



                console.log(
                    "Skipped edges:",
                    skippedEdges
                );



                console.log(
                    "Graph:",
                    graph.order,
                    graph.size
                );






                // -----------------------
                // Sigma
                // -----------------------

                const container =
                    document.getElementById(
                        "sigma-container"
                    );



                const sigma =
                    new Sigma(
                        graph,
                        container,
                        {

                            renderLabels:
                                false,

                            defaultNodeColor:
                                "#999999"


                        }
                    );







                // -----------------------
                // Node reducer
                // -----------------------

                sigma.setSetting(
                    "nodeReducer",
                    (node, data) => {



                        // no selection

                        if (
                            !selectedNode
                        ) {

                            return data;

                        }




                        // collaborator-only mode

                        if (
                            collaboratorsOnly
                            &&
                            !highlightedNodes.has(node)
                        ) {

                            return {

                                ...data,

                                hidden:
                                    true

                            };

                        }




                        // selected performer

                        if (
                            node === selectedNode
                        ) {


                            return {

                                ...data,

                                color:
                                    "#ffcc00",

                                label:
                                    data.label

                            };

                        }





                        // collaborators

                        if (
                            highlightedNodes.has(node)
                        ) {


                            return {

                                ...data,

                                color:
                                    "#dddddd"

                            };

                        }



                        return data;



                    }
                );








                // -----------------------
                // Edge reducer
                // -----------------------

                sigma.setSetting(
                    "edgeReducer",
                    (edge, data) => {



                        if (
                            highlightedEdges.has(edge)
                        ) {


                            return {

                                ...data,

                                hidden:
                                    false,

                                color:
                                    "rgba(0, 0, 0, 0.7)"

                            };

                        }



                        return {

                            ...data,

                            hidden:
                                true

                        };


                    }
                );







                // -----------------------
                // Search index
                // -----------------------

                const performerIndex = {};



                graph.forEachNode(
                    (node, attributes) => {


                        performerIndex[
                            attributes.label
                            .toLowerCase()
                        ] = node;


                    }
                );





                // -----------------------
                // Focus function
                // -----------------------

                function focusNode(node) {


                    selectedNode = node;


                    highlightedNodes =
                        new Set();


                    highlightedEdges =
                        new Set();



                    highlightedNodes.add(node);




                    graph.forEachEdge(
                        node,
                        (
                            edge,
                            attributes,
                            source,
                            target
                        ) => {



                            highlightedEdges.add(
                                edge
                            );


                            const otherNode =
                                source === node
                                ?
                                target
                                :
                                source;



                            highlightedNodes.add(
                                otherNode
                            );


                        }
                    );



                    sigma.refresh();





                    // move camera without zoom

                    const displayData =
                        sigma.getNodeDisplayData(
                            node
                        );


                    sigma.getCamera()
                        .animate(
                        {

                            x:
                                displayData.x,

                            y:
                                displayData.y

                        },
                        {

                            duration:
                                1000

                        }
                    );


                }








                // -----------------------
                // Search
                // -----------------------

                document
                    .getElementById(
                        "searchButton"
                    )
                    .addEventListener(
                        "click",
                        () => {



                            const query =
                                document
                                .getElementById(
                                    "search"
                                )
                                .value
                                .toLowerCase()
                                .trim();



                            const node =
                                performerIndex[query];



                            if (!node) {

                                alert(
                                    "Performer not found"
                                );

                                return;

                            }



                            focusNode(node);



                        }
                    );








                // -----------------------
                // Click
                // -----------------------

                sigma.on(
                    "clickNode",
                    ({node}) => {


                        focusNode(node);


                    }
                );







                // -----------------------
                // Toggle
                // -----------------------

                document
                    .getElementById(
                        "collaboratorToggle"
                    )
                    .addEventListener(
                        "change",
                        (event) => {


                            collaboratorsOnly =
                                event.target.checked;


                            sigma.refresh();


                        }
                    );







                // -----------------------
                // Clear
                // -----------------------

                document
                    .getElementById(
                        "clearButton"
                    )
                    .addEventListener(
                        "click",
                        () => {



                            selectedNode = null;


                            highlightedNodes =
                                new Set();


                            highlightedEdges =
                                new Set();



                            collaboratorsOnly =
                                false;



                            document
                            .getElementById(
                                "collaboratorToggle"
                            )
                            .checked = false;



                            sigma.refresh();


                        }
                    );





                console.log(
                    "Sigma loaded!"
                );


            }

        });


    }

});