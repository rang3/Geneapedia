$(function(){ // on dom ready

// photos from flickr with creative commons license
console.log("Page Loaded!");
var cy = cytoscape({
  container: document.getElementById('cy'),
  
  boxSelectionEnabled: false,
  autounselectify: true,
   wheelSensitivity: 0.1,
  
  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'height': 'data(popularity)',
        'width': 'data(popularity)',
        'background-fit': 'cover',
        'border-color': '#000',
        'border-width': 3,
        'border-opacity': 0.5
      })
    .selector('edge')
      .css({
        'width': 6,
        'target-arrow-shape': 'triangle',
        'line-color': 'data(faveColor)',
        'target-arrow-color': 'data(faveColor)',
        'curve-style': 'bezier'
      })
    .selector('#Steve')
      .css({
        'background-image': 'https://upload.wikimedia.org/wikipedia/commons/b/b9/Steve_Jobs_Headshot_2010-CROP.jpg'
      })
    .selector('#Laurene')
      .css({
        'background-image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Laurene_Powell_Jobs.jpg/220px-Laurene_Powell_Jobs.jpg'
      })
    .selector('#Chrisann')
      .css({
        'background-image': 'http://i.dailymail.co.uk/i/pix/2015/08/07/16/2B2E51CA00000578-3188738-image-m-35_1438959595262.jpg'
      })
  .selector('#Reed')
      .css({
        'background-image': 'http://enewsdaily.info/now/wp-content/uploads/2012/09/Reed-Jobs-Powell-Steve-Jobs-son_pic_thumb.jpg'
      })
  .selector('#Eve')
      .css({
        'background-image': 'http://thedailytruffle.com/wp-content/uploads/2015/10/Eve-Jobs-dress.jpg'
      })
  .selector('#Lisa')
      .css({
        'background-image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Lisa_Brennan-Jobs.jpg/220px-Lisa_Brennan-Jobs.jpg'
      }),
  
  elements: {
    nodes: [
      { data: { id: 'Steve', name: 'Steve Jobs' , birth: 'February 24, 1955', death: 'October 5, 2011', alma: 'Reed College', popularity: '300'} },
      { data: { id: 'Laurene', name: 'Laurene Powell', birth: 'November 6, 1963', death: 'N/A', alma: 'Stanford University', popularity: '100' } },
      { data: { id: 'Chrisann', name: 'Steve Jobs' , birth: 'September 29, 1954', death: 'N/A', alma: ' ', popularity: '50'} },
      { data: { id: 'Reed', name: 'Reed Jobs' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50'} },
      { data: { id: 'Eve', name: 'Eve Jobs' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50' } },
      { data: { id: 'Lisa', name: 'Lisa Brennan-Jobs' , birth: 'May 17, 1978', death: 'N/A', alma: 'Harvard University', popularity: '150' } },
      { data: { id: 'Erin', name: 'Erin Jobs' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50'} },
      { data: { id: 'Paul', name: 'Paul Jobs' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50' } },
      { data: { id: 'Clara', name: 'Clara Jobs' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50' } },
    ],
    edges: [
      { data: { source: 'Steve', target: 'Reed' , faveColor: '#ffaaaa'} },
      { data: { source: 'Steve', target: 'Eve' , faveColor: '#ffaaaa'} },
      { data: { source: 'Steve', target: 'Reed' , faveColor: '#ffaaaa'} },
      { data: { source: 'Steve', target: 'Eve' , faveColor: '#ffaaaa'} },
      { data: { source: 'Steve', target: 'Lisa' , faveColor: '#ffaaaa'} },
      { data: { source: 'Steve', target: 'Erin' , faveColor: '#ffaaaa'} },
      { data: { source: 'Laurene', target: 'Reed' , faveColor: '#ffaaaa'} },
      { data: { source: 'Laurene', target: 'Lisa' , faveColor: '#ffaaaa'} },
      { data: { source: 'Laurene', target: 'Eve' , faveColor: '#ffaaaa'} },
      { data: { source: 'Chrisann', target: 'Erin' , faveColor: '#ffaaaa'} }
    ]
  },
  
  layout: {
    name: 'breadthfirst',
    directed: true,
    padding: 10
  }
}); // cy init
  cy.nodes().forEach(function(n){

    n.qtip({
      content: {title: n.data('name'), text: "Birth Date: " + n.data('birth') + "\n" + "Death Date: " + n.data('death') + "\n" + "Alma Mater: " + n.data('alma') + "\n" + "Popularity Score: " + n.data('popularity')},
      position: {
        my: 'top left',
        at: 'right center'
      },
      style: {
        classes: 'qtip-bootstrap',
        tip: {
          width: 16,
          height: 8,
        } 
      }
    });
  });

  cy.add({
    group: "edges",
    data: { source: 'Steve', target: 'Laurene' , faveColor: '#aaffaa'}
  });

  cy.add({
    group: "edges",
    data: { source: 'Steve', target: 'Chrisann' , faveColor: '#aaffaa'}
  });

  cy.add({
    data: { source: 'Steve', target: 'Clara' , faveColor: '#aaaaff'}
  });

  cy.add({
    data: { source: 'Steve', target: 'Paul' , faveColor: '#aaaaff'}
  });

  cy.$('#Clara').position({
  x: cy.$('#Steve').position('x') - 200,
  y: cy.$('#Steve').position('y') - 400
});

  cy.$('#Paul').position({
  x: cy.$('#Steve').position('x') + 200,
  y: cy.$('#Steve').position('y') - 400
});

}); // on dom ready