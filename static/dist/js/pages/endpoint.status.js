$(function () {
    // Initialize Datatables
    $('.table').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": false,
      "info": true,
      "autoWidth": false,
      "responsive": true,
    });

    // Clear sessionstorage
    // Get all endpoints and their urls + client IP address
    // Store the endpoints in a session storage
    sessionStorage.clear();
    $.ajax({
      url: '/mweb/get-endpoints',
      type: 'GET',
      dataType:'json',
      success: function(response){
        var endpoints = response['endpoints'];
        for (i = 0; i < endpoints.length; i++) {
          sessionStorage.setItem(endpoints[i][1], endpoints[i][2]);
        };
      }
    });
    console.log(sessionStorage);


  // async sample
  // $('#check-statusdown').click(function(){
  //     //1. Create a new function that returns a promise
  //     function firstFunction() {
  //       return new Promise((resolve, reject) => {
  //           let y = 0
  //           setTimeout(() => {
  //             for(i=0; i<10; i++){
  //                y++
  //             }
  //              console.log('loop completed')  
  //              resolve(y)
  //           }, 2000)
  //       })
  //     }
      
  //     //2. Create an async function
  //     async function secondFunction() {
  //         console.log('before promise call')
  //         //3. Await for the first function to complete
  //         let result = await firstFunction()
  //         console.log('promise resolved: ' + result)
  //         console.log('next step')
  //     }; 

  //     secondFunction();
  // });



  // prod - status check routines
  function checkStatus(url){
    return new Promise ((resolve, reject) => {
    var address = url;
    var t1 = Date.now();
    var t2;
    var max = 2000;
    var failed = false;
    // initialize xhr object
    var httpReq = (window.XMLHttpRequest)?new XMLHttpRequest():new ActiveXObject("Microsoft.XMLHTTP");
    // action on readystate changes
    httpReq.onreadystatechange = function() {
        var failTimer = setTimeout(function() {
                            failed = true;
                            httpReq.abort();
                            }, 
                        max);

        if (httpReq.readyState == 4) {
            if (!failed && (httpReq.status == 200 || httpReq.status == 0)) {
                clearTimeout(failTimer);
                t2 = Date.now();
                var timeTotal = (t2 - t1);
                rtt = timeTotal.toString() + ' ms';
                resolve(['up', rtt]);
            }
            else {
                resolve(['down', '0']);
            }
        }
    }
    // open and send xhr request
    try {
    httpReq.open("GET", address, true);
    httpReq.send(null);
    } catch(e) {
        console.log("Error retrieving data httpReq. Some browsers only accept cross-domain request with HTTP.");
    }
    })
  };

  // gather site information from Session storage
  function collectSites(){
    return new Promise ((resolve, reject) => {
        let endpoints = new Object();
        setTimeout(() => {
          for(i=0; i<sessionStorage.length; i++) {
            let site = sessionStorage.key(i);
            let address = sessionStorage.getItem(site);
            endpoints[site] = address;
          }; 
          resolve(endpoints);
        }, 1000)
    })
  };

  // Get website status and update table
  async function get_status(){
    let sites = await collectSites();
    // console.log(sites);
    let status = {};
    for (const [key, value] of Object.entries(sites)) {
      let address = value;
      status[key] = {'url': address, 'status':'down', 'rtt': '0'};
      let result = await checkStatus(address);
      if (result[0] == 'up') {
        status[key]['status'] = 'up';
        status[key]['rtt'] = result[1];
      };
      // console.log(key);  '<a href="" target="_blank" data-toggle="tooltip" title="'+ value['url'] +'">'+ key +'</a>', 
    }
    // console.log(status);
    var table_reachable = $("#reachable").DataTable();
    table_reachable.clear().draw();
    var table_unreachable = $("#unreachable").DataTable();
    table_unreachable.clear().draw();
    // update reachability status in the tables
    for (const [key, value] of Object.entries(status)) {
      if (value['status'] == 'up') {
        table_reachable.row.add([
          '<a href="'+ value['url'] +'" target="_blank" data-toggle="tooltip" title="'+ value['url'] +'">'+ key +'</a>', 
          value['rtt'], 
          '<i class="far fa-arrow-alt-circle-up" style="font-size: 24px; color: green;"></i>'
        ]).draw();
      } else {
        table_unreachable.row.add([
          '<a href="'+ value['url'] +'" target="_blank" data-toggle="tooltip" title="'+ value['url'] +'">'+ key +'</a>', 
          '<i class="far fa-arrow-alt-circle-down" style="font-size: 24px; color: red;"></i>'
        ]).draw();
      }
    }
    // current time
    var timeNow = new Date();
    var hours   = timeNow.getHours();
    var minutes = timeNow.getMinutes();
    var seconds = timeNow.getSeconds();
    var timeString = "" + ((hours > 12) ? hours - 12 : hours);
    timeString  += ((minutes < 10) ? ":0" : ":") + minutes;
    timeString  += ((seconds < 10) ? ":0" : ":") + seconds;
    timeString  += (hours >= 12) ? " P.M." : " A.M.";
    // update last updated time
    $("#reachable_updated").html(timeString);
    $("#unreachable_updated").html(timeString);
  };

  // get monitoring interval
  function getInterval(){

    return new Promise ((resolve, reject) => {

      $.ajax({
        url: '/srm/get-interval?type=http',
        type: 'GET',
        dataType:'json',
        success: function(response){
          let interval = response['interval'];
          let monitoring_interval = parseInt(interval, 10) * 60 * 1000
          resolve(monitoring_interval);
        }
      });
    })

  };

  async function Interval(){
    get_status();
    let interval = await getInterval();
    console.log(interval);
    // execute status checking task once every 2 minutes
    window.setInterval(function(){
      get_status();
    }, interval);
  }

  Interval();

});