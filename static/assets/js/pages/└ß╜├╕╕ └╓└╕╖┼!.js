$(document).ready(function() {
    var statable = $('#EOT-data-entry-list').DataTable( {
        "ordering": false,
        'rowsGroup': [0,1],
        'bStateSave': true,
        /*initComplete: function () {
            this.api().columns([0, 1]).every( function () {
                var column = this;
                var colTitle = this.header().innerHTML;
                var select = $('<select><option value="" selected>' + colTitle + '</option></select>')
                    .appendTo( $(column.header()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );

                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option>'+d+'</option>' )
                } );
            } );
        }*/
    } );
    var statable2 = $('#stop-enroll-table').DataTable( {
        "ordering": false,
        'rowsGroup': [0,1],
        'bStateSave': true,
        /*initComplete: function () {
            this.api().columns([0, 1]).every( function () {
                var column = this;
                var colTitle = this.header().innerHTML;
                var select = $('<select><option value="" selected>' + colTitle + '</option></select>')
                    .appendTo( $(column.header()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );

                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option>'+d+'</option>' )
                } );
            } );
        }*/
    } );	
	$('#table-filter2').on('change', function(){
       statable.search(this.value).draw();   
    });
	$('#table-filter3').on('change', function(){
       statable.search(this.value).draw();   
    });
	$('#table-filter4').on('change', function(){
       statable2.search(this.value).draw();   
    });
	$('#table-filter5').on('change', function(){
       statable2.search(this.value).draw();   
    });

    /*
    var statable3 =$('#withdrawal-list').DataTable( {
        "ordering": false,
        'bStateSave': true,
        initComplete: function () {
            this.api().columns([1]).every( function () {
                var column = this;
                var colTitle = this.header().innerHTML;
                var select = $('<select><option value="" selected>' + colTitle + '</option></select>')
                    .appendTo( $(column.header()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );

                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option>'+d+'</option>' )
                } );
            } );

        }
    } );*/
	$('#table-filter').on('change', function(){
       statable3.search(this.value).draw();   
    });

    $('#status-discord-list, #no-data-entry-in-the-last-week, #data-entry-list').DataTable( {
        dom: 'Bfrtip',
        buttons: [{
            extend: 'excel',
            title: 'Status 불일치 명단',
            text: '엑셀 다운로드'
        }],
        'paging': true,
        'ordering': false,
        initComplete: function () {
            this.api().columns([]).every( function () {
                var column = this;
                var colTitle = this.header().innerHTML;
                var select = $('<select><option value="" selected>' + colTitle + '</option></select>')
                    .appendTo( $(column.header()).empty() )
                    .on( 'change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search( val ? '^'+val+'$' : '', true, false )
                            .draw();
                    } );

                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option>'+d+'</option>' )
                } );
            } );

        }
    } );


} );

    // 날짜 포맷("yyyy-MM-dd") 형식으로 반환
    dateFormatter = function(newDay, today) {
      let year = newDay.getFullYear();
      let month = newDay.getMonth()+1;
      let date = newDay.getDate();

      // 기존 날짜와 새로운 날짜가 다른 경우
      if (today) {
        let todayDate = today.getDate()

        if(date != todayDate) {
          if (month == 0)
            year-=1
            month = (month + 11) % 12
            date = new Date(year, month, 0).getDate() // 해당 달의 마지막 날짜 반환
        }
      }

      month = ("0"+month).slice(-2);
      date = ("0"+date).slice(-2);

      return year+"-"+month+"-"+date
    }

    $('#myTab a').on('click', function (e) {
      $(this).tab('show')
    })

    $( document ).ready(function() {
      $('.flip').click(function() {
        $(this)
          .closest('tbody')
          .next('.section')
          .toggle('fast')

        $(this)
          .toggleClass('active')
      });
    });

    
    var series = [
        {
          name: 'IIT',
          data: ['0', '0']
        }, {
          name: 'SIT',
          data: ['2', '0']
        }, {
          name: 'PMS',
          data: ['0', '1']
        }, {
          name: 'EAP',
          data: ['0', '0']
        }, {
          name: 'Palliative',
          data: ['0', '0']
        }, {
          name: 'Blood',
          data: ['0', '0']
        }, {
          name: 'ETC',
          data: ['0', '0']
        },
    ];
    
    var options_crc_research_count = {
      series,
      chart: {
        type: "bar",
        height: 550,
        stacked: true,
        toolbar: {
          show: false
        },
        events: {
          mounted: (chartContext, config) => {
            console.log("mounted", chartContext, config, config.globals.yRange);
              addAnnotations(config);
          },
          updated: (chartContext, config) => {
              addAnnotations(config);
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: {
                fontSize: '10px',
                colors: ["#304758"]
            }
      },
      colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#bcf60c', '#6c757d'],
      plotOptions: {
        bar: {
          columnWidth: '50%',
          dataLabels: {
            maxItems: 2,
            position: 'center',
          }
        }
      },
      xaxis: {
        categories: ['백은실', '이윤정'],
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        // floating: true,
        labels: {
          // maxHeight: 0,
          hideOverlappingLabels: false,
        }
      },
      yaxis: {
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        labels: {
          hideOverlappingLabels: true,
        }
      },
      fill: {
        opacity: 1
      },
      legend: {
        position: "top",
        horizontalAlign: "left"
      },
      grid: {
        padding: {
          left: 13.5,
          right: 0
        },
        xaxis: {
            lines: {
                show: true
            }
        },
      }
    };

    var crc_research_count_dashboard = new ApexCharts(document.querySelector("#crc_research_count_dashboard"), options_crc_research_count);
    crc_research_count_dashboard.render();

    const addAnnotations = (config) => {
      const ongoing = ['2', '2'];
      const seriesTotals = config.globals.stackedSeriesTotals;
      const isHorizontal = options.plotOptions.bar.horizontal;
      chart.clearAnnotations();

      try {
        categories.forEach((category, index) => {
          chart.addPointAnnotation(
            {
              y: isHorizontal
                ? calcHorizontalY(config, index)
                : seriesTotals[index],
              x: isHorizontal ? 0 : category,
              label: {
                text: `${ongoing[index]}명`
          }
            },
            false
          );

          if (isHorizontal) {
            adjustPointAnnotationXCoord(config, index);
          }
        });
      } catch (error) {
        console.log(`Add point annotation error: ${error.message}`);
      }
    };

    const calcHorizontalY = (config, index) => {
      const catLength = categories.length;
      const yRange = config.globals.yRange[0];
      const minY = config.globals.minY;
      const halfBarHeight = yRange / catLength / 2;

      return minY + halfBarHeight + 2 * halfBarHeight * (catLength - 1 - index);
    };

    const adjustPointAnnotationXCoord = (config, index) => {
      const gridWidth = config.globals.gridWidth;
      const seriesTotal = config.globals.stackedSeriesTotals[index];
      const minY = config.globals.minY;
      const yRange = config.globals.yRange[0];
      const xOffset = (gridWidth * (seriesTotal + Math.abs(minY))) / yRange;
      const labelField = document.querySelector(
        `.apexcharts-point-annotations rect:nth-of-type(${index + 1}`
      );
      const labelFieldXCoord = parseFloat(labelField.getAttribute("x"));
      const text = document.querySelector(
        `.apexcharts-point-annotations text:nth-of-type(${index + 1}`
      );

      labelField.setAttribute("x", labelFieldXCoord + xOffset);
      text.setAttribute("x", xOffset);
      console.log(labelFieldXCoord);
    };


    // Total Visit Count - Normal Distribution (전체)
    var options2 = {
        series: [
          {
            name: "CRC 수",
            data: "{{ total_visit_count_normalization.TOTAL_visit_series_list|join:', ' }}"
          }
        ],
        chart: {
          height: 350,
          type: 'area',
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          enabled: true,
        },
        stroke: {
          curve: 'smooth'
        },
        grid: {
          borderColor: '#e7e7e7',
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        markers: {
          size: 1
        },
        xaxis: {
          type: 'category',
          categories: "{{ total_visit_count_normalization.TOTAL_visit_xaxis_list }}",
          title: {
              text: 'Total Visit Count (CLUE/GSI/의무기록사)',
          },
        },
        tooltip: {
          shared: true,
          intersect: false,
          y: [{
            formatter: function (y) {
            if(typeof y !== "undefined") {
              return  y.toFixed(0) + " 명";
            }
              return y;
            }
          }]
        },
        yaxis: {
          title: {
            text: 'CRC 수 (명)'
          },
        },
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          floating: true,
          offsetY: -25,
          offsetX: -5
        }
    };

    var chart2 = new ApexCharts(
        document.querySelector("#visit-count-normalization-dashboard"),
            options2
        );
    chart2.render();

    // Total Visit Count - Normal Distribution (CLUE 팀)
    var options3 = {
        series: [
          {
            name: "CRC 수 - CLUE",
            data: "{{ total_visit_count_normalization.CLUE_visit_series_list|join:', ' }}"
          }
        ],
        chart: {
          height: 350,
          type: 'area',
          toolbar: {
            show: false
          },
        },
        dataLabels: {
          enabled: true,
        },
        stroke: {
          curve: 'smooth'
        },
        grid: {
          borderColor: '#e7e7e7',
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        markers: {
          size: 1
        },
        xaxis: {
          type: 'category',
          categories: "{{ total_visit_count_normalization.CLUE_visit_xaxis_list }}",
          title: {
              text: 'CLUE',
          },
        },
        tooltip: {
          shared: true,
          intersect: false,
           y: [{
             formatter: function (y) {
             if(typeof y !== "undefined") {
               return  y.toFixed(0) + " 명";
             }
               return y;
             }
           }]
        },
        yaxis: {
          title: {
            text: 'CRC 수 (명) - CLUE'
          },
        },
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          floating: true,
          offsetY: -25,
          offsetX: -5
        }
    };

    var chart3 = new ApexCharts(
        document.querySelector("#visit-count-clue-normalization-dashboard"),
        options3
    );
    chart3.render();

    // Total Visit Count - Normal Distribution (GSI 팀)
    var options4 = {
        series: [
          {
            name: "CRC 수 - GSI",
            data: "{{ total_visit_count_normalization.GSI_visit_series_list|join:',' }}"
          }
        ],
        chart: {
          height: 350,
          type: 'area',
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          enabled: true,
        },
        stroke: {
          curve: 'smooth'
        },
        grid: {
          borderColor: '#e7e7e7',
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        markers: {
          size: 1
        },
        xaxis: {
          type: 'category',
          categories: "{{ total_visit_count_normalization.GSI_visit_xaxis_list }}",
          title: {
              text: 'GSI',
          },
        },
        tooltip: {
          shared: true,
          intersect: false,
          y: [{
            formatter: function (y) {
            if(typeof y !== "undefined") {
                return  y.toFixed(0) + " 명";
            }
                return y;
            }
          }]
        },
        yaxis: {
          title: {
            text: 'CRC 수 (명) - GSI'
          },
        },
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          floating: true,
          offsetY: -25,
          offsetX: -5
        }
    };

    var chart4 = new ApexCharts(
        document.querySelector("#visit-count-gsi-normalization-dashboard"),
        options4
    );
    chart4.render();

    var options5 = {
        series: [
          {
            name: "",
            data: ['-100']
          }
        ],
        chart: {
          height: 600,
          type: 'bar',
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          enabled: true,
          formatter: function (y) {
            if(typeof y !== "undefined") {
                return  y.toFixed(0) + " %";
            }
                return y;
          }
        },
        markers: {
          size: 1
        },
        xaxis: {
          categories: ['이윤정'],
          title: {
              text: '',
          },
        },
        yaxis: [
          {
            labels: {
              formatter: function(val) {
                return val;
              }
            }
          }
        ],
        tooltip: {
          shared: true,
          intersect: false,
          y: [{
            formatter: function (y) {
            if(typeof y !== "undefined") {
                return  y + " %";
            }
                return y;
            }
          }]
        },
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          floating: true,
          offsetY: -25,
          offsetX: -5
        }
    };

    var chart5 = new ApexCharts(
        document.querySelector("#cycle-visit-count-QOQ"),
        options5
    );
    chart5.render();

    // CRC별  진행 환자 수
    var N_of_ongoings_by_CRC_PI_option = {
      series: [
      ],
      chart: {
        type: "bar",
        height: 550,
        stacked: true,
        toolbar: {
          show: false
        },
        events: {
          mounted: (chartContext, config) => {
            console.log("mounted", chartContext, config, config.globals.yRange);
              addAnnotations(config);
          },
          updated: (chartContext, config) => {
              addAnnotations(config);
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: {
                fontSize: '10px',
                colors: ["#304758"]
            }
      },
      colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#bcf60c', '#6c757d', '#aab2bd'],
      plotOptions: {
        bar: {
          columnWidth: '50%',
          dataLabels: {
            maxItems: 2,
            position: 'center',
          }
        }
      },
      xaxis: {
        categories: ['이윤정', '이윤정'],
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        // floating: true,
        labels: {
          // maxHeight: 0,
          hideOverlappingLabels: false,
        }
      },
      yaxis: {
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        labels: {
          hideOverlappingLabels: true,
        }
      },
      fill: {
        opacity: 1
      },
      legend: {
        position: "top",
        horizontalAlign: "left"
      },
      grid: {
        padding: {
          left: 13.5,
          right: 0
        },
        xaxis: {
            lines: {
                show: true
            }
        },
      }
    };

    var N_of_ongoings_by_CRC_PI_dict = new ApexCharts(document.querySelector("#N_of_ongoings_by_CRC_PI_dict_dashboard"), N_of_ongoings_by_CRC_PI_option);
    N_of_ongoings_by_CRC_PI_dict.render();

    // PI별 진행 환자 수
    var N_of_ongoings_by_PI_CRC_option = {
      series: [
      ],
      chart: {
        type: "bar",
        height: 700,
        stacked: true,
        toolbar: {
          show: false
        },
        events: {
          mounted: (chartContext, config) => {
            console.log("mounted", chartContext, config, config.globals.yRange);
              addAnnotations(config);
          },
          updated: (chartContext, config) => {
              addAnnotations(config);
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: {
                fontSize: '10px',
                colors: ["#304758"]
            }
      },
      colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#bcf60c', '#6c757d', '#aab2bd'],
      plotOptions: {
        bar: {
          columnWidth: '50%',
          dataLabels: {
            maxItems: 2,
            position: 'center',
          }
        }
      },
      xaxis: {
        categories: [],
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        // floating: true,
        labels: {
          // maxHeight: 0,
          hideOverlappingLabels: false,
        }
      },
      yaxis: {
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        labels: {
          hideOverlappingLabels: true,
        }
      },
      fill: {
        opacity: 1
      },
      legend: {
        position: "top",
        horizontalAlign: "left"
      },
      grid: {
        padding: {
          left: 13.5,
          right: 0
        },
        xaxis: {
            lines: {
                show: true
            }
        },
      }
    };

    var N_of_ongoings_by_PI_CRC_dict = new ApexCharts(document.querySelector("#N_of_ongoings_by_PI_CRC_dict_dashboard"), N_of_ongoings_by_PI_CRC_option);
    N_of_ongoings_by_PI_CRC_dict.render();

    // PI별 담당 연구 개수
    var PI_research_count_option = {
      chart: {
        type: "bar",
        height: 550,
        stacked: true,
        toolbar: {
          show: false
        },
        events: {
          mounted: (chartContext, config) => {
            console.log("mounted", chartContext, config, config.globals.yRange);
              addAnnotations(config);
          },
          updated: (chartContext, config) => {
              addAnnotations(config);
          }
        }
      },
      series: [
      ],
      dataLabels: {
        enabled: true,
        style: {
                fontSize: '10px',
                colors: ["#304758"]
            }
      },
      colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#bcf60c', '#6c757d'],
      plotOptions: {
        bar: {
          columnWidth: '50%',
          dataLabels: {
            maxItems: 2,
            position: 'center',
          }
        }
      },
      xaxis: {
        categories: [],
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        // floating: true,
        labels: {
          // maxHeight: 0,
          hideOverlappingLabels: false,
        }
      },
      yaxis: {
        axisTicks: {
          show: true
        },
        axisBorder: {
          show: true
        },
        labels: {
          hideOverlappingLabels: true,
        }
      },
      fill: {
        opacity: 1
      },
      legend: {
        position: "top",
        horizontalAlign: "left"
      },
      grid: {
        padding: {
          left: 13.5,
          right: 0
        },
        xaxis: {
            lines: {
                show: true
            }
        },
      }
    };

    var PI_research_count = new ApexCharts(document.querySelector("#PI_research_count_dashboard"), PI_research_count_option);
    PI_research_count.render();

    var chkValue = $('input[type=radio][name=optionRadios]:checked').val();
    if(chkValue == 'total'){
            $( '#fromDate' ).attr('disabled', 'disabled').val('');
            $( '#toDate' ).attr('disabled', 'disabled').val('');
        }

    $('input[type=radio][name=optionRadios]').on('click',function () {
        var chkValue = $('input[type=radio][name=optionRadios]:checked').val();
        var recruitingSelect = document.getElementById("is_recruiting");

        if(chkValue == 'total'){
            $( '#fromDate' ).attr('disabled', 'disabled').val('');
            $( '#toDate' ).attr('disabled', 'disabled').val('');
        }
        else if(chkValue != 'total'){
            $( '#fromDate' ).removeAttr('disabled');
            $( '#toDate' ).removeAttr('disabled');
        }

        if(chkValue == 'period'){
            recruitingSelect.disabled = true;
        }
        else if(chkValue != 'period'){
            recruitingSelect.disabled = false;
        }
    });

    $(function() {
        $( "#fromDate" ).datepicker({
          dateFormat: "yy-mm-dd"
        });
        $( "#toDate" ).datepicker({
          dateFormat: "yy-mm-dd"
        });
        $('.menu').menuBar();
    });

    (function() {
      $.fn.menuBar = function(){
        this.each(function(index){
          var $menuBar = null,
              $menuList = null,
              $menuSelect = null;

          function init(el){
            $menuBar = $(el);
            $menuList = $menuBar.find('li');
          }
          function event(){
            $menuList.on('click', function(){
              if($menuSelect)
                $menuSelect.removeClass('active');
                $menuList.removeClass('active');
              $menuSelect = $(this);
              $menuSelect.addClass('active');
              $menuSelect.parent('ul').next().children().eq($(this).index()).show().siblings().hide();
            });
          }
          init($(this));
          event();
        })
        return this;
      }
    })(jQuery);