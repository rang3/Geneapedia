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
        'background-image': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'
      })
    .selector('#Laurene')
      .css({
        'background-image': 'https://upload.wikimedia.org/wikipedia/commons/e/ec/Melinda_Gates_-_World_Economic_Forum_Annual_Meeting_2011.jpg'
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
        'background-image': ''
      }),
  
  elements: {
    nodes: [
      { data: { id: 'Steve', name: 'Bill Gates' , birth: 'October 28, 1955', death: 'N/A', alma: 'Harvard College', popularity: '300'} },
      { data: { id: 'Laurene', name: 'Melinda Gates', birth: 'August 5, 1964', death: 'N/A', alma: 'Duke University', popularity: '100' } },
      { data: { id: 'Reed', name: '' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50'} },
      { data: { id: 'Eve', name: '' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50' } },
      { data: { id: 'Lisa', name: '' , birth: 'May 17, 1978', death: 'N/A', alma: 'Harvard University', popularity: '150' } },
      { data: { id: 'Paul', name: 'William H. Gates Sr.' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50' } },
      { data: { id: 'Clara', name: 'Mary Maxwell Gates' , birth: 'N/A', death: 'N/A', alma: 'N/A', popularity: '50' } },
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
