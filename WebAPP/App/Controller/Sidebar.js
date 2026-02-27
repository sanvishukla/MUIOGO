import { GROUPNAMES, PARAMORDER, PARAMCOLORS, RESULTPARAMORDER, RESULTPARAMCOLORS, RESULTGROUPNAMES } from "../../Classes/Const.Class.js";
import { Model } from "../Model/Sidebar.Model.js";
import { Osemosys } from "../../Classes/Osemosys.Class.js";
import { Message } from "../../Classes/Message.Class.js";

export class Sidebar {
    static Reload(casename) {
        Osemosys.getData(casename, 'genData.json')
        .then(genData => {
            const promise = [];
            promise.push(genData);
            const PARAMETERS = Osemosys.getParamFile();
            promise.push(PARAMETERS);
            const VARIABLES = Osemosys.getParamFile('Variables.json');
            promise.push(VARIABLES);
            const RESULTEXISTS = Osemosys.resultsExists(casename);
            promise.push(RESULTEXISTS);
            return Promise.all(promise);
        })
        .then(data => {
            let [genData, PARAMETERS, VARIABLES, RESULTEXISTS] = data;
            let model = new Model(PARAMETERS,VARIABLES, genData, RESULTEXISTS);
            this.initAppRoutes(model);
            this.initEvents();
            // Notify that sidebar menu population is complete
            try { window.dispatchEvent(new Event('sidebarReady')); } catch(e) {}
        })
        .catch(error => {
            Message.danger(error);
            // Ensure app doesn't stay hidden if sidebar population fails
            try { window.dispatchEvent(new Event('sidebarReady')); } catch(e) {}
        });
    }

    static initAppRoutes(model) {
        $('#dynamicRoutes').empty();
        $('.dynamicRoutesLink').hide();
        $('.dynamicRoutesRES').hide();
        $('.dynamicResults').hide();

        //console.log('model menu ', model)

        if (model.menu) {

            //Routes.addRoutes(model.PARAMETERS);
            $('.dynamicRoutesLink').show();
            //RES prikazi samo ako ima IAR ili OAR
            if ( model.menuCondition.IAR || model.menuCondition.OAR) {
                $('.dynamicRoutesRES').show();
            }else{
                $('.dynamicRoutesRES').hide();
            }
            let res = `
            <label class="input" style="display:block; margin-left:11px">
                <i class="ace-icon white fa fa-search nav-search-icon"></i>
                <input type="text" placeholder="Search ..." class="nav-search-input" id="MenuSearch" />
                
            </label>`;
            $('#dynamicRoutes').append(res);

            //console.log('model sidebar ', model)

            $.each(PARAMORDER, function (id, group) {
                $.each(model.PARAMETERS[group], function (id, obj) {
                    //da li ima parametara definisanih za grupu
                    if (model.PARAMETERS[group] !== undefined || model.PARAMETERS[group].length != 0) {
                        if (obj.menu) {
                            // console.log('obj.id ', obj.id)
                            if (obj.id == 'IAR' && model.menuCondition.IAR) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'OAR' && model.menuCondition.OAR) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'INCR' && model.menuCondition.INCR) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'ITCR' && model.menuCondition.ITCR) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'EAR' && model.menuCondition.EAR) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'CCM' && model.menuCondition.CM) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'CNCM' && model.menuCondition.CM) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'CAM' && model.menuCondition.CM) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }
                            if (obj.id == 'UCC' && model.menuCondition.CM) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }

                            if (['OLS', 'SLS', 'CCS', 'RSC', 'MSC', 'TTS', 'TFS', 'DS', 'DIDT' ].includes(obj.id)&& model.menuCondition.STG) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }

                            else if (!model.menuGroup.includes(obj.id)) {
                                let res = `
                                <li  class="">
                                    <a href="#/${group}/${obj.id}" class="menu-items" title="${GROUPNAMES[group]}">
                
                                    ${obj.value}
                                    <span class="badge badge-sm inbox-badge bg-color-${PARAMCOLORS[group]} align-top hidden-mobile pull-right"><small>${group}</small></span>
                                    </a>
                                </li>`;
                                $('#dynamicRoutes').append(res);
                            }

                        }
                    }
                });
            });
        } 
        if(model.ResultsMenu){
            $('.dynamicResults').show();
        }
    }

    static initEvents() {
        $('#Navi > li').click(function (e) {
            e.stopPropagation();
            $('li').removeClass('active');
            //$(selector).removeClass('open');
            $(this).addClass('active');
        });

        $('#Navi > li >ul>li').click(function (e) {
            e.stopPropagation();
            $('li').removeClass('active');
            //$(selector).removeClass('open');
            $(this).parent().closest("li").addClass('active');
            $(this).addClass('active');
        });

        //Search menu
        $('#MenuSearch').keyup(function () {
            var query = $.trim($('#MenuSearch').val()).toLowerCase();
            $('.menu-items').each(function () {
                var $this = $(this);
                if ($this.text().toLowerCase().indexOf(query) === -1)
                    $this.closest('li').fadeOut();
                else $this.closest('li').fadeIn();
            });
        });

        // Update active state based on current page
        this.updateActiveState();
    }

    /**
     * Update the sidebar active state based on current page ID from localStorage or hash
     */
    static updateActiveState() {
        // Wait for sidebar to be available in DOM
        const checkSidebar = () => {
            // Check if sidebar navigation exists
            if ($('#Navi').length === 0) {
                // Sidebar not loaded yet, retry after a short delay
                setTimeout(checkSidebar, 50);
                return;
            }

            // Get current page ID from localStorage
            let currentPageId = localStorage.getItem("osy-pageId");
            
            if (!currentPageId) {
                // If not in localStorage, try to get from current hash
                let hash = window.location.hash;
                if (hash && hash.length > 1) {
                    // Extract page id from hash (e.g., #/AddCase -> AddCase, #/R/id -> R)
                    let parts = hash.substring(2).split('/');
                    currentPageId = parts[0];
                } else {
                    currentPageId = "Home";
                }
            }

            // Remove active class from all menu items
            $('#Navi li').removeClass('active');

            // Find and activate the correct menu item
            if (currentPageId === 'Home') {
                $('#Navi li:first').addClass('active');
            } else {
                // Search through all menu items for matching link
                $('#Navi a').each(function() {
                    let href = $(this).attr('href');
                    
                    // Check if this link matches the current page
                    if (href && (href.includes(`#/${currentPageId}`) || href === `#/${currentPageId}`)) {
                        let $li = $(this).closest('li');
                        $li.addClass('active');
                        
                        // Also activate parent if this is a nested item
                        $li.parents('li').addClass('active');
                    }
                });
            }
        };

        // Start the check
        checkSidebar();
    }
}