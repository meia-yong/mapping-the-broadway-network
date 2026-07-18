import Graph from "graphology";
import Sigma from "sigma";
import Papa from "papaparse";
import Fuse from "fuse.js"


const graph = new Graph();


const DATA_FILE =
    `${import.meta.env.BASE_URL}data/drl_linear_1_15.csv`;

const EDGE_FILE =
    `${import.meta.env.BASE_URL}data/performer_edges_clean.csv`;

const METADATA_FILE =
    `${import.meta.env.BASE_URL}data/performer_metadata.csv`;


let selectedNode = null;

let highlightedNodes = new Set();

let highlightedEdges = new Set();

let collaboratorsOnly = false;

let performerMetadata = {};


Papa.parse(DATA_FILE, {

    download: true,
    header: true,

    complete: (nodeResults) => {


        console.log(
            "Loaded nodes:",
            nodeResults.data.length
        );


        nodeResults.data.forEach((row) => {

            graph.addNode(
                row.id,
                {
                    x: Number(row.x),
                    y: Number(row.y),
                    size: Number(row.size),
                    label: row.performer_name,
                    color: "rgba(120,120,120,0.7)"
                }
            );

        });



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
                            weight: Number(row.weight)
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

                Papa.parse(METADATA_FILE, {

                    download: true,
                    header: true,

                    complete: (metadataResults) => {


                        console.log(
                            "Loaded metadata:",
                            metadataResults.data.length
                        );


                        metadataResults.data.forEach(
                            (row) => {

                                performerMetadata[
                                    row.performer_id
                                ] = row;

                            }
                        );



                const container =
                    document.getElementById(
                        "sigma-container"
                    );


                const sigma =
                    new Sigma(
                        graph,
                        container,
                        {
                            renderLabels: false,
                            defaultNodeColor: "#999999"
                        }
                    );



                sigma.setSetting(
                    "nodeReducer",
                    (node, data) => {


                        if (!selectedNode) {

                            return data;

                        }


                        if (
                            collaboratorsOnly &&
                            !highlightedNodes.has(node)
                        ) {

                            return {
                                ...data,
                                hidden: true
                            };

                        }


                        if (node === selectedNode) {

                            return {
                                ...data,
                                color: "#ffcc00",
                                label: data.label
                            };

                        }


                        if (
                            highlightedNodes.has(node)
                        ) {

                            return {
                                ...data,
                                color: "#dddddd"
                            };

                        }


                        return data;


                    }
                );



                sigma.setSetting(
                    "edgeReducer",
                    (edge, data) => {


                        if (
                            highlightedEdges.has(edge)
                        ) {

                            return {
                                ...data,
                                hidden: false,
                                color: "rgba(0,0,0,0.7)"
                            };

                        }


                        return {
                            ...data,
                            hidden: true
                        };


                    }
                );



                const performerIndex = new Map();
                const performerNames = [];
                let fuse;


                graph.forEachNode(
                    (node, attributes) => {

                        const name =
                            attributes.label;


                        performerIndex.set(
                            name.toLowerCase(),
                            node
                        );


                        performerNames.push(name);

                    }
                );


                fuse = new Fuse(
                    performerNames,
                    {
                        threshold: 0.3,
                        includeScore: true
                    }
                );


                function showPerformerPanel(metadata) {

                    if (!metadata) {
                        console.log("No metadata found");
                        return;
                    }

                    document.getElementById("panel-name").textContent =
                        metadata.performer_name;

                    document.getElementById("panel-career").textContent =
                        `${metadata.first_year}–${metadata.last_year}`;

                    document.getElementById("panel-productions").textContent =
                        metadata.production_count;

                    document.getElementById("panel-collaborators").textContent =
                        metadata.collaborator_count;    

                    document
                        .getElementById("performer-panel")
                        .classList.remove("hidden");

                }

                function hidePerformerPanel() {

                    document
                        .getElementById("performer-panel")
                        .classList
                        .add("hidden");

                }

                function focusNode(node) {


                    selectedNode = node;

                    document
                    .getElementById(
                        "searchInput"
                    )
                    .value =
                        graph.getNodeAttribute(
                            node,
                            "label"
                        );

                    highlightedNodes = new Set();

                    highlightedEdges = new Set();


                    highlightedNodes.add(node);



                    graph.forEachEdge(
                        node,
                        (
                            edge,
                            attributes,
                            source,
                            target
                        ) => {


                            highlightedEdges.add(edge);


                            const otherNode =
                                source === node
                                ? target
                                : source;


                            highlightedNodes.add(
                                otherNode
                            );


                        }
                    );


                    sigma.refresh();

                    showPerformerPanel(node);

                    const displayData =
                        sigma.getNodeDisplayData(
                            node
                        );


                    sigma.getCamera()
                        .animate(
                            {
                                x: displayData.x,
                                y: displayData.y
                            },
                            {
                                duration: 1000
                            }
                        );


                }



                function findPerformer() {


                    const query =
                        document
                        .getElementById(
                            "searchInput"
                        )
                        .value
                        .toLowerCase()
                        .trim();



                    const node =
                        performerIndex.get(query);



                    if (!node) {

                        alert(
                            "Performer not found"
                        );

                        return;

                    }


                    focusNode(node);


                }



                const searchButton =
                    document.getElementById(
                        "searchButton"
                    );


                const searchInput =
                    document.getElementById(
                        "searchInput"
                    );


                searchButton.addEventListener(
                    "click",
                    findPerformer
                );


                searchInput.addEventListener(
                    "keydown",
                    (event) => {

                        if (
                            event.key === "Enter"
                        ) {

                            findPerformer();

                        }

                    }
                );

                const suggestions =
                    document.getElementById(
                        "suggestions"
                    );


                searchInput.addEventListener(
                    "input",
                    () => {


                        const query =
                            searchInput.value
                                .toLowerCase()
                                .trim();


                        suggestions.innerHTML = "";


                        if (!query) {

                            return;

                        }


                        const matches =
                            fuse.search(query)
                                .map(result => result.item)
                                .sort((a, b) => {


                                    const aLower =
                                        a.toLowerCase();

                                    const bLower =
                                        b.toLowerCase();


                                    const aStarts =
                                        aLower.startsWith(query);

                                    const bStarts =
                                        bLower.startsWith(query);


                                    const aLast =
                                        aLower
                                        .split(" ")
                                        .slice(1)
                                        .some(
                                            part =>
                                            part.startsWith(query)
                                        );


                                    const bLast =
                                        bLower
                                        .split(" ")
                                        .slice(1)
                                        .some(
                                            part =>
                                            part.startsWith(query)
                                        );


                                    return (
                                        bStarts - aStarts ||
                                        bLast - aLast
                                    );


                                })
                                .slice(0,50);



                        matches.forEach(
                            name => {


                                const item =
                                    document.createElement(
                                        "div"
                                    );


                                item.className =
                                    "suggestion-item";


                                item.textContent =
                                    name;


                                item.addEventListener(
                                    "click",
                                    () => {

                                        searchInput.value =
                                            name;


                                        suggestions.innerHTML =
                                            "";


                                        findPerformer();

                                    }
                                );


                                suggestions.appendChild(
                                    item
                                );


                            }
                        );


                    }
                );



                sigma.on("clickNode", ({ node }) => {

                    focusNode(node);

                    const performerID = node.replace("A_", "");
                    const metadata = performerMetadata[performerID];

                    if (metadata) {
                        showPerformerPanel(metadata);
                    }

                });



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

                            hidePerformerPanel();

                            collaboratorsOnly = false;

                            document
                            .getElementById("searchInput")
                            .value = "";


                            document
                            .getElementById(
                                "collaboratorToggle"
                            )
                            .checked = false;


                            sigma.refresh();


                        }
                    );



                const loadingScreen =
                    document.getElementById(
                        "loading-screen"
                    );


                if (loadingScreen) {

                    loadingScreen.classList.add(
                        "hidden"
                    );

                }


                console.log(
                    "Sigma loaded!"
                );


            }

        });

        }

    });


    }

});