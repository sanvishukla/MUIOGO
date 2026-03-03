
export class Model {
    constructor (casename, genData, resData, pageId) {
      if(casename && genData && resData){

        let cases = resData['osy-cases'];
        let scenarios =  genData['osy-scenarios'];
        //let scenarios =  resData['osy-cases'][0]['Scenarios']
        let cs = null;

        let scMap = {};
        if (scenarios) {
          $.each(scenarios, function (id, sc) {
            scMap[sc.ScenarioId] = sc;
          });
        }

        let scBycs = {};
        if (resData['osy-cases']) {
          $.each(resData['osy-cases'], function (id, cs) {
            scBycs[cs.Case] = cs.Scenarios
          });
        }

        //26.04.2023. VK
        //dodati eventualno nove scenarije koji su dodani poslije uspjesnog RUN-a i nema ih u resData
        //pored originalnih scenarija u caserunu, potrebno dodati eventualno nove 
        //scenarije koji su dodani poslije uspjesnog RUN-a, kao neaktivne
        let sccsMap = {};
        if (cases && scBycs) {
          $.each(cases, function (CsId, csObj) {

            if (!(csObj.Case in sccsMap))
              {sccsMap[csObj.Case] = {}}
            if (scBycs[csObj.Case]) {
                $.each(scBycs[csObj.Case], function (id, scObj) {
                    sccsMap[csObj.Case][scObj.ScenarioId] = scObj;
                });
            }

            if (scenarios) {
                $.each(scenarios, function (key, obj) {
                    if(obj.ScenarioId in sccsMap[csObj.Case] === false){
                        let sc = JSON.parse(JSON.stringify(obj));
                        sc.Active = false;
                        scBycs[csObj.Case].push(sc);
                    }
                });
            }
          });
        }

        this.casename = casename;
        this.cs = cs;
        this.scBycs = scBycs;
        this.title = "Run model";
        this.scenarios = scenarios;
        this.scenariosCount = scenarios ? scenarios.length : 0;
        this.scMap = scMap;
        this.cases = cases;
        this.pageId = pageId;
      }else{
        this.casename = null;
        this.title = "Generate data file";
        this.scenarios = null;
        this.pageId = pageId;
      }
    }
}
