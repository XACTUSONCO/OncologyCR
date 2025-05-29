$(document).ready(function() {
    /*var statable = $('#EOT-data-entry-list').DataTable( {
        "ordering": false,
        'rowsGroup': [0,1],
        'bStateSave': true,
        initComplete: function () {
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
        }
    } );*/
    /*
    var statable2 = $('#stop-enroll-table').DataTable( {
        "ordering": false,
        'rowsGroup': [0,1],
        'bStateSave': true,
        initComplete: function () {
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
        }
    } );*/
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


    // PI별 진행 환자 수
    /*
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
    */

    // PI별 담당 연구 개수
    /*
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
    */

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
        $( "#strtDate" ).datepicker({
          dateFormat: "yy-mm-dd"
        });
        $( "#endDate" ).datepicker({
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