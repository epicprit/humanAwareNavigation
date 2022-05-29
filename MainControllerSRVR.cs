using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#if UNITY_EDITOR
using UnityEditor;
#endif

using System.IO;
using System.Text;
using System.Linq;
using UnityEngine.UI;
using Newtonsoft.Json;
using System;

//  new input system:
using UnityEngine.InputSystem;
using UnityEngine.XR.Interaction.Toolkit;


/* this is new: */
using Valve.VR; // steamVR pluging 2.7. 2021/10/18
/* ---- */


using System.Diagnostics;


[System.Serializable]
public class Trial {

    public int delay_ms;
    public Robot robot;

    // This is for the declarations of processing JSON Files
    public List<Human> humans;
    public List<Object> objects;
    public List<Wall> walls;
    public Floor floor;


}


public class Robot {
    public float[] position;
    public float[] rotation;
}

public class Human {
    public string id;
    public float[] position;
    public float[] rotation;
}

public class Contents
{
    public List<Object> inside;
    public List<Object> on_top;
    public List<Object> underneath;
}


public class Object
{
    public string id;
    public string model;
    public float[] position;
    public float[] rotation;
    public Contents contents;

    public Vector3 getPositionVector()
    {

        Vector3 myVector = new Vector3(-1, -1, -1);
        if (position != null)
        {
            if (position.Length == 3)
            {
                myVector.x = position[0];
                myVector.y = position[1];
                myVector.z = position[2];
            }
        }
        return myVector;

    }
    public Vector3 getRotationVector()
    {

        Vector3 myVector = new Vector3(-1, -1, -1);
        if (rotation != null)
        {
            if (rotation.Length == 3)
            {
                myVector.x = rotation[0];
                myVector.y = rotation[1];
                myVector.z = rotation[2];
            }
        }
        return myVector;

    }




}

public class Wall
{
    public float[] center;
    public float[] size;
}

public class Floor
{
    public float[] center;
    public float[] size;
}


public class ExperimentConfig {
    public List<float[]> array1;
    public List<Trial> trials;

    public ExperimentConfig() {
        array1 = new List<float[]>();
        trials = new List<Trial>();
    }



    public Trial getTrial(int iIndex) {
        if (iIndex < 0 || iIndex > trials.Count - 1) {
            iIndex = 0;
        }
        return trials.ElementAt(iIndex);
    }

    public int nrTrials() {
        return trials.Count;
    }

}

public class MainControllerSRVR : MonoBehaviour {

    public Text textInstructions;
    //    public Text textThanks;
    //    public MenuManager menuManager;

    private bool m_ShowDebugMainController;

    public const string strSettingDebugMainController = "Debug Main Controller";
    //    public Text InputDelay;

    //   //-- private Text textUI;
    //    //--private TextAsset txtAssetPause;
    //    private TextAsset txtAssetThanks;

    private bool bBlank;
    private Canvas canvasBlocker;

    public bool useHMD;

    public Canvas canvasInput;
    public Canvas canvasUI;
    public GameObject rig;


    public Slider sliderInput;
    private ExperimentConfig experimentConfig;


    public static bool expRunning;
    //    public static bool expPaused;
    //    public static string currentTarget;
    //    public static string currentTargetPpn;

    // world references every item and character from the JSON file. Very useful for the updating the world
    private Dictionary<string, GameObject> world; 
    public GameObject robotico;
    private GameObject[] arrHumans;
    private List<GameObject> arrObjects;
    //private List<GameObject> arrWalls;
    private GameObject[] arrLights;
    private GameObject oFloor;
    private GameObject oRoot;
 
   


    /*
    public XRController rightHand;
    public InputHelpers.Button button;
    */


    // https://sarthakghosh.medium.com/a-complete-guide-to-the-steamvr-2-0-input-system-in-unity-380e3b1b3311
    private SteamVR_Input_Sources handType;


    public SteamVR_Action_Boolean SubmitAnswer;
    public SteamVR_Action_Vector2 MoveSlider;

    private bool bTriggerPulled;
    





    //    List<string> lCharNames;
    //    List<GameObject> lCharacters;

    //    public HMDRecord hmdRecord;

    public static bool IsEnabledDebug {
        get { return Convert.ToBoolean(PlayerPrefs.GetInt(strSettingDebugMainController)); }
        set { PlayerPrefs.SetInt(strSettingDebugMainController, Convert.ToInt16(value)); }

    }

    //    private void LightTargetFires(bool b) {
    //        GameObject[] gos = GameObject.FindGameObjectsWithTag("target");
    //        foreach (GameObject go in gos) {
    //            VRInteractiveItemTarget cc = (VRInteractiveItemTarget)go.GetComponent(typeof(VRInteractiveItemTarget));
    //            cc.TurnFireOn(b);
    //        }
    //    }


    /* this is the new way to do this...*/

    /* this works!
    public void TriggerUp(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource) {
        Debug.Log("Trigger is up");
    }
    */
    public void TriggerDown(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource) {
        UnityEngine.Debug.Log("Trigger is down");
        bTriggerPulled = true;
    }


    /* methods to be called from `Steam VR_Behaviour_Boolean`
    public void aaaa(SteamVR_Behaviour_Boolean fromAction, SteamVR_Input_Sources fromSource, Boolean bb) {
        Debug.Log("aaaaaaaaaaaaaaaa");
    }

    public void bbbb(SteamVR_Behaviour_Vector2 fromAction, SteamVR_Input_Sources fromSource, Vector2 aa, Vector2 bb) {
        Debug.Log("aaaaaaaaaaaaaaaa");
        Debug.Log("a: " + aa.ToString());
        Debug.Log("b: " + bb.ToString());
    }
    */



    void Start() {





        m_ShowDebugMainController = true;
        bTriggerPulled = false;

        canvasInput.enabled = false;

        handType = SteamVR_Input_Sources.Any;

        SubmitAnswer.AddOnStateDownListener(TriggerDown, handType);
        expRunning = false;

        m_ShowDebugMainController = IsEnabledDebug;

        if (m_ShowDebugMainController) {
            print("MainController::Start()");
        }


        GameObject go = GameObject.Find("Canvas");
        if (go != null) {
            canvasBlocker = go.GetComponent<Canvas>();
        } else {
#if UNITY_EDITOR
                    EditorUtility.DisplayDialog("Error", "Canvas not found", "OK");
#endif
            Application.Quit();
        }


        setScreenBlack(true);

        if (world == null)
        {
            world = new Dictionary<string, GameObject>();
        }
            
        //arrWalls = GameObject.FindGameObjectsWithTag("Wall");
        //UnityEngine.Debug.Log("MainController found " + arrWalls.Length.ToString() + " walls in scene");
        arrObjects = new List<GameObject>();
        //UnityEngine.Debug.Log("MainController found " + arrObjects.Length.ToString() + " objects in scene");
        GameObject[] roots = GameObject.FindGameObjectsWithTag("Root");
        if (roots.Length == 1) {
            oRoot = roots[0];
        }
        GameObject[] floors = GameObject.FindGameObjectsWithTag("Floor");
        //oFloor.transform.localScale = new Vector3(0.1f, 1.0f, 0.1f);
        if (floors.Length == 1)
        {
            oFloor = floors[0];

           
        }
        arrLights = GameObject.FindGameObjectsWithTag("Spotlight");

        UnityEngine.Debug.Log("MainController found " + arrLights.Length.ToString() + " lights in scene");

        robotico = GameObject.FindWithTag("Robot");
        Vector3 hide_me = new Vector3(-20, -20, -20);
        robotico.transform.position = hide_me;

        arrHumans = GameObject.FindGameObjectsWithTag("Human");
        foreach (GameObject h in arrHumans)
        {
            h.transform.position = hide_me;
        }

        
        int ll = arrHumans.Length;

        UnityEngine.Debug.Log("MainController found " + ll.ToString() + " humans in scene");

        foreach (object o in world)
        {
            ( (GameObject) o).transform.position = hide_me;
        }


        //--canvasUI.enabled = true;

        //        TextAsset txtAssetInstructions;
        //        string strFNInstructions = System.IO.Path.Combine(Application.streamingAssetsPath, "Instructions.txt");
        //        if (!File.Exists(strFNInstructions)) {
        //            string strErrorMessage = "Error:\n\"" + strFNInstructions + "\"\ndoes not exist";
        //            txtAssetInstructions = new TextAsset(strErrorMessage);
        //        } else {
        //            txtAssetInstructions = new TextAsset(System.IO.File.ReadAllText(strFNInstructions, Encoding.GetEncoding("iso-8859-1")));
        //        }

        //        //textUI.text = txtAssetInstructions.text;
        //        textInstructions.text = txtAssetInstructions.text;

        //        string strFNThanks = System.IO.Path.Combine(Application.streamingAssetsPath, "Thanks.txt");
        //        if (!File.Exists(strFNThanks)) {
        //            string strErrorMessage = "Error:\n\"" + strFNThanks + "\"\ndoes not exist";
        //            txtAssetThanks = new TextAsset(strErrorMessage);
        //        } else {
        //            txtAssetThanks = new TextAsset(System.IO.File.ReadAllText(strFNThanks, Encoding.GetEncoding("iso-8859-1")));
        //        }
        //        textThanks.text = txtAssetThanks.text;


        //        //--expPaused = false;




        // Set working directory and create process
        // var workingDirectory = Path.GetFullPath("Scripts");
        var process = new Process
		{
			StartInfo = new ProcessStartInfo
			{
				FileName = "cmd.exe",
				RedirectStandardInput = true,
				RedirectStandardOutput = true,
				UseShellExecute = false,
				WorkingDirectory = "C:\\Users\\180123614\\Anaconda3"
			}
		};
		process.Start();
		// Pass multiple commands to cmd.exe
		using (var sw = process.StandardInput)
		{
			if (sw.BaseStream.CanWrite)
			{
				// Vital to activate Anaconda
				sw.WriteLine("C:\\Users\\180123614\\Anaconda3\\Scripts\\activate.bat");
				sw.WriteLine("python C:\\Users\\180123614\\Documents\\SocialRobotVRPritesh\\Assets\\Scripts\\main.py");
			}
		}
		
// System.Threading.Thread.Sleep(1000);

// read multiple output lines
// while (!process.StandardOutput.EndOfStream)
// {
    // var line = process.StandardOutput.ReadLine();
    // Console.WriteLine(line);
// }	
		
        ProcessStartInfo start = new ProcessStartInfo();
		start.FileName = "C:\\Users\\180123614\\Anaconda3\\python.exe";
		start.Arguments = "C:\\Users\\180123614\\Documents\\SocialRobotVRPritesh\\Assets\\Scripts\\main.py";
		start.WorkingDirectory = "C:\\Users\\180123614\\Anaconda3";
	    start.UseShellExecute = false;
		start.RedirectStandardOutput = true;
		using(Process process2 = Process.Start(start))
	    {
			using(StreamReader reader = process2.StandardOutput)
			{
				string result = reader.ReadToEnd();
				Console.Write(result);
 				UnityEngine.Debug.Log(result);
			}
		}
 		
		
        string strFNJSON = System.IO.Path.Combine(Application.streamingAssetsPath, "C:\\Users\\180123614\\Documents\\output.json");
        // Debug.Log("strFNJSON: " + strFNJSON);

        if (!File.Exists(strFNJSON)) {
            string strErrorMessage = "Error:\nExperiment configuration\n\"" + strFNJSON + "\"\nnot found";
            //--textUI.text = strErrorMessage;
#if UNITY_EDITOR
                EditorUtility.DisplayDialog("Error", strErrorMessage, "OK");
#endif
        } else {
            string strJSON = System.IO.File.ReadAllText(strFNJSON);
            experimentConfig = JsonConvert.DeserializeObject<ExperimentConfig>(strJSON);

        }



        //TEMP   StartCoroutine(DelayExperimentStart());
        //setScreenBlack(false);

    }

   

    GameObject createObjectFromJSONNode(Object thisObject)
    {


        Vector3 vObjectRotation = thisObject.getRotationVector();  
            Vector3 vObjectPosition = thisObject.getPositionVector();
        string model = null;

            if (thisObject.model != null)
            {
                model = thisObject.model;
            }
            /*if (thisObject.position.Length == 3)
            {
                vObjectPosition.x = thisObject.position[0];
                vObjectPosition.y = thisObject.position[1];
                vObjectPosition.z = thisObject.position[2];
            }

            if (thisObject.rotation.Length == 3)
            {
                vObjectRotation.x = thisObject.rotation[0];
                vObjectRotation.y = thisObject.rotation[1];
                vObjectRotation.z = thisObject.rotation[2];
            }*/



            if ("Chair".Equals(thisObject.model))
            {
                UnityEngine.Debug.Log("Chair" + thisObject.id + vObjectPosition.ToString());
                GameObject newChair = Instantiate(GameObject.FindWithTag("Chair"));
                newChair.transform.position = vObjectPosition;
                newChair.transform.eulerAngles = vObjectRotation;
                newChair.tag = "ChairClone";

                arrObjects.Add(newChair);
           
        

                return newChair;

            }

            else if ("Clock".Equals(thisObject.model))
            {
                UnityEngine.Debug.Log("Clock" + thisObject.id + vObjectPosition.ToString());
                GameObject newClock = Instantiate(GameObject.FindWithTag("Clock"));
                newClock.transform.position = vObjectPosition;
                newClock.transform.eulerAngles = vObjectRotation;
                newClock.tag = "ClockClone";

                arrObjects.Add(newClock);

            return newClock;


            }

            else if ("Desk".Equals(thisObject.model))
            {
                UnityEngine.Debug.Log("Desk" + thisObject.id + vObjectPosition.ToString());
                GameObject newDesk = Instantiate(GameObject.FindWithTag("Desk"));
                newDesk.transform.position = vObjectPosition;
                newDesk.transform.eulerAngles = vObjectRotation;
                newDesk.tag = "DeskClone";

                arrObjects.Add(newDesk);
                if (thisObject.contents != null)
                {
                    Contents c = thisObject.contents;
                    UnityEngine.Debug.Log("Found this many items underneath Desk" + c.underneath.Count.ToString());
                    UnityEngine.Debug.Log("Found this many items on_top Desk" + c.on_top.Count.ToString());


                    foreach (Object childObject in c.on_top)
                    {
                        GameObject content_object = createObjectFromJSONNode(childObject);
                        content_object.transform.SetParent(newDesk.transform, false);
                        if (content_object != null)
                    {
                        world[childObject.id] = content_object;
                    }


                    }

                    foreach (Object childObject in c.underneath)
                    {
                        GameObject content_object = createObjectFromJSONNode(childObject);
                        content_object.transform.SetParent(newDesk.transform, false);
                        if (content_object != null)
                        {
                            world[childObject.id] = content_object;
                        }

                }
            }

            return newDesk;


            }

            else if ("Shelf".Equals(thisObject.model))
            {
                UnityEngine.Debug.Log("Shelf" + thisObject.id + vObjectPosition.ToString());
                GameObject newShelf = Instantiate(GameObject.FindWithTag("Shelf"));
                newShelf.transform.position = vObjectPosition;
                newShelf.transform.eulerAngles = vObjectRotation;
                newShelf.tag = "ShelfClone";

                arrObjects.Add(newShelf);
                if (thisObject.contents != null)
                {
                    Contents c = thisObject.contents;
                    UnityEngine.Debug.Log("Found this many items inside Shelf" + c.inside.Count.ToString());
                    UnityEngine.Debug.Log("Found this many items on_top Shelf" + c.on_top.Count.ToString());

                    foreach (Object childObject in c.on_top)
                    {
                        GameObject content_object = createObjectFromJSONNode(childObject);
                        content_object.transform.SetParent(newShelf.transform, false);
                        if (content_object != null)
                        {
                            world[childObject.id] = content_object;
                        }

                }

                    foreach (Object childObject in c.inside)
                    {
                        GameObject content_object = createObjectFromJSONNode(childObject);
                        content_object.transform.SetParent(newShelf.transform, false);
                        if (content_object != null)
                        {
                            world[childObject.id] = content_object;
                        }

                }
            }

            return newShelf;


            }

            else if ("Bookcase".Equals(thisObject.model))
            {
                UnityEngine.Debug.Log("Bookcase" + thisObject.id + vObjectPosition.ToString());
                GameObject newBookcase = Instantiate(GameObject.FindWithTag("Bookcase"));
                newBookcase.transform.position = vObjectPosition;
                newBookcase.transform.eulerAngles = vObjectRotation;
                newBookcase.tag = "BookcaseClone";

                arrObjects.Add(newBookcase);
                if (thisObject.contents != null)
                {
                    Contents c = thisObject.contents;
                    UnityEngine.Debug.Log("Found this many items inside Bookcase" + c.inside.Count.ToString());
                    UnityEngine.Debug.Log("Found this many items on_top Bookcase" + c.on_top.Count.ToString());
                    
                    foreach(Object childObject in c.on_top)
                    {
                        GameObject content_object = createObjectFromJSONNode(childObject);
                        content_object.transform.SetParent(newBookcase.transform, false);
                        if (content_object != null)
                        {
                            world[childObject.id] = content_object;
                        }

                }

                    foreach (Object childObject in c.inside)
                    {
                        GameObject content_object = createObjectFromJSONNode(childObject);
                        content_object.transform.SetParent(newBookcase.transform, false);
                        if (content_object != null)
                        {
                            world[childObject.id] = content_object;
                        }

                }
            }

                return newBookcase;
            }

            else if ("Plant".Equals(thisObject.model))
            {

                    UnityEngine.Debug.Log("Plant" + thisObject.id + vObjectPosition.ToString());
                    GameObject newPlant = Instantiate(GameObject.FindWithTag("Plant"));
                    newPlant.transform.position = vObjectPosition;
                    newPlant.transform.eulerAngles = vObjectRotation;
                    newPlant.tag = "PlantClone";

                    arrObjects.Add(newPlant);
                    return newPlant;



                

            }

            else if ("Boots".Equals(thisObject.model))
            {

                UnityEngine.Debug.Log("Boots" + thisObject.id + vObjectPosition.ToString());
                GameObject newBoots = Instantiate(GameObject.FindWithTag("Boots"));
                newBoots.transform.position = vObjectPosition;
                newBoots.transform.eulerAngles = vObjectRotation;
                newBoots.tag = "BootsClone";

                arrObjects.Add(newBoots);
                return newBoots;





            }

            else if ("Bowl".Equals(thisObject.model))
            {

                UnityEngine.Debug.Log("Bowl" + thisObject.id + vObjectPosition.ToString());
                GameObject newBowl = Instantiate(GameObject.FindWithTag("Bowl"));
                newBowl.transform.position = vObjectPosition;
                newBowl.transform.eulerAngles = vObjectRotation;
                newBowl.tag = "BowlClone";

                arrObjects.Add(newBowl);
                return newBowl;





            }

            else if ("Mug".Equals(thisObject.model))
            {

                UnityEngine.Debug.Log("Mug" + thisObject.id + vObjectPosition.ToString());
                GameObject newMug = Instantiate(GameObject.FindWithTag("Mug"));
                newMug.transform.position = vObjectPosition;
                newMug.transform.eulerAngles = vObjectRotation;
                newMug.tag = "MugClone";

                arrObjects.Add(newMug);
                return newMug;





            }

        else
            {
                UnityEngine.Debug.Log("object was found but wasn't a chair or plant" + thisObject.id + vObjectPosition.ToString());


            }

        return null;


        

    }

    void Update() {
        if (m_ShowDebugMainController) {
            print("MainController::Update()");
        }


       
        var keyboard = Keyboard.current;

        if (keyboard.bKey.wasPressedThisFrame) {
            UnityEngine.Debug.Log("expCtrl::Update::B");
            toggleBlankScreen();
        }

        if (keyboard.spaceKey.wasPressedThisFrame) {
            //Debug.Log("expCtrl::Update::Space");
            UnityEngine.Debug.Log("+++++STARTING EXPERIMENT+++++");
            StartExperimentCoroutine();
        }


        //if (Input.GetKeyDown(KeyCode.Alpha1)) {
        //    Debug.Log("press 1");
        //    PlayAudioCue.audioPlayer.playAudioCue(1);
        //    turnAllHeads("target01");
        //} else if (Input.GetKeyDown(KeyCode.Alpha2)) {
        //    Debug.Log("press 2");
        //    PlayAudioCue.audioPlayer.playAudioCue(2);
        //    turnAllHeads("target02");
        //} /*else if (Input.GetKeyDown(KeyCode.Alpha3)) {
        //    Debug.Log("press 3");
        //    PlayAudioCue.audioPlayer.playAudioCue(3);
        //    turnAllHeads("target03");
        //} else if (Input.GetKeyDown(KeyCode.Alpha4)) {
        //    Debug.Log("press 4");
        //    PlayAudioCue.audioPlayer.playAudioCue(3);
        //    turnAllHeads("target04");
        //} */ else if (Input.GetKeyDown(KeyCode.Alpha5)) {
        //    Debug.Log("press 5");
        //    turnAllHeads("Panel");
        //    //resetAllHeads();
        //}
    }


    IEnumerator RunExperiment() {
        expRunning = true;

        if (m_ShowDebugMainController) {
            print("MainController::RunExperiment()");
        }

		textInstructions.text = "press enter to continue";

        //int iCurrentTrial = PlayerPrefs.GetInt("currentTrial");
        //iCurrentTrial = iCurrentTrial + 1;

        //if (iCurrentTrial >= experimentConfigSingleTrial.nrTrials()) {
        //    iCurrentTrial = 1;
        //}


        //PlayerPrefs.SetInt("currentTrial", iCurrentTrial);
        //LogManager.instance.WriteEntry("currentTrial:" + iCurrentTrial);


        List<Trial> lstTrials = experimentConfig.trials;

        foreach (Trial trial in lstTrials) {

            /* PROCEDURE
             * 1 POSITION HUMANS
             * 2 POSITION ROBOT
             * 3 UN BLANK
             * 4 WAIT 
             * 5 BLANK
             * 6 SHOW INPUT PANEL
             * 7 GOTO 1
             */

            bTriggerPulled = false;

            int delay_ms = trial.delay_ms;


            Floor floor = trial.floor;
            Vector3 vFloorCenter = new Vector3(-99, -99, -99);
            Vector3 vFloorSize = new Vector3(-99, -99, -99);

            UnityEngine.Debug.Log("size[0]" + floor.size[0].ToString());
            UnityEngine.Debug.Log("size[1]" + floor.size[1].ToString());
            UnityEngine.Debug.Log("size[2]" + floor.size[2].ToString());

            if (floor.size.Length == 3)
            {
                vFloorSize.x = floor.size[0]*0.1f;
                vFloorSize.y = floor.size[1];
                vFloorSize.z = floor.size[2]*0.1f;
            }
            UnityEngine.Debug.Log("vFloorSize" + vFloorSize.ToString());
            UnityEngine.Debug.Log("center" + floor.center.ToString());

            if (floor.center.Length == 3)
            {
                vFloorCenter.x = floor.center[0];
                vFloorCenter.y = floor.center[1];
                vFloorCenter.z = floor.center[2];
            }
            UnityEngine.Debug.Log("vFloorCenter" + vFloorCenter.ToString());

            oFloor.transform.localScale = vFloorSize;
            oFloor.transform.position = vFloorCenter;


            List<Wall> walls = trial.walls;
            int wallCount = 0;
            int numWalls = walls.Count;

            foreach (Wall wall in walls)
            {
                Vector3 vWallCenter = new Vector3(-99, -99, -99);
                Vector3 vWallSize = new Vector3(-99, -99, -99);

                UnityEngine.Debug.Log("size[0]" + wall.size[0].ToString());
                UnityEngine.Debug.Log("size[1]" + wall.size[1].ToString());
                UnityEngine.Debug.Log("size[2]" + wall.size[2].ToString());

                if (wall.size.Length == 3)
                {
                    vWallSize.x = wall.size[0];
                    vWallSize.y = wall.size[1];
                    vWallSize.z = wall.size[2];
                }
                UnityEngine.Debug.Log("vWallSize" + vWallSize.ToString());
                UnityEngine.Debug.Log("center" + wall.center.ToString());

                if (wall.center.Length == 3)
                {
                    vWallCenter.x = wall.center[0];
                    vWallCenter.y = wall.center[1];
                    vWallCenter.z = wall.center[2];
                }
                UnityEngine.Debug.Log("vWallCenter" + vWallCenter.ToString());

                List<GameObject> cubes = new List<GameObject>();

              

                
                GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
                // Set color
                Renderer cubeRender = cube.GetComponentsInChildren<Renderer>()[0];
                cubeRender.material.color = new Color(0.95f, 0.95f, 0.95f);
              

                // Set possition
                cube.name = "Wall "+ wallCount.ToString() + " :: center " + vWallCenter.ToString() + ",  size:" + vWallSize.ToString();
                cube.transform.localScale = vWallSize;
                cube.transform.position = vWallCenter;
                //cube.transform.SetParent(oRoot.transform);
                cubes.Add(cube);
              

                

            

                wallCount++;

            }
                
            float[] intervals = { 0.16f, 0.50f, 0.84f };

            int numLights = 0;
            foreach(GameObject light in arrLights)
            {
                int row = (int) numLights/3;
                int col = numLights%3;

                Vector3 vLightPosition = new Vector3(floor.size[0] * intervals[col], 4, floor.size[2] * intervals[row]);
                UnityEngine.Debug.Log("light" + numLights.ToString() + "position" + vLightPosition.ToString());
                light.transform.position = vLightPosition;




                numLights++;
            }

            //Camera.main.transform.position = new Vector3(floor.size[0]/2.0f, 1.74f, 0.2f);




            List<Human> humans = trial.humans;

            int maxHumans = arrHumans.Length;
            int ii = 0;
            foreach (Human human in humans) {

                
                

                Vector3 vHumanRotation = new Vector3(-99, -99, -99);
                Vector3 vHumanPosition = new Vector3(-99, -99, -99);

                if (human.position.Length == 3) {
                    vHumanPosition.x = human.position[0];
                    vHumanPosition.y = human.position[1];
                    vHumanPosition.z = human.position[2];
                }

                if (human.rotation.Length == 3) {
                    vHumanRotation.x = human.rotation[0];
                    vHumanRotation.y = human.rotation[1];
                    vHumanRotation.z = human.rotation[2];
                }


                if (ii < maxHumans) {

                    
                    UnityEngine.Debug.Log("humans"+ ii.ToString() + "humanPosition" + vHumanPosition.ToString());
                    arrHumans[ii].transform.position = vHumanPosition;
                    arrHumans[ii].transform.eulerAngles = vHumanRotation;
                    world[human.id] = arrHumans[ii];
                }

                ii++;
        

            }

            Robot robot = trial.robot;
            Vector3 vRobotRotation = new Vector3(-99, -99, -99);
            Vector3 vRobotPosition = new Vector3(-99, -99, -99);

            if (robot.position.Length == 3) {
                vRobotPosition.x = robot.position[0];
                vRobotPosition.y = robot.position[1];
                vRobotPosition.z = robot.position[2];
            }

            if (robot.rotation.Length == 3) {
                vRobotRotation.x = robot.rotation[0];
                vRobotRotation.y = robot.rotation[1];
                vRobotRotation.z = robot.rotation[2];
            }


            if (robotico != null) {
                robotico.transform.position = vRobotPosition;
                robotico.transform.eulerAngles = vRobotRotation;
                world["robot"] = robotico;
            }

            List<Object> objects = trial.objects;

            foreach (Object thisObject in objects)
            {

                if (world.ContainsKey(thisObject.id))
                {
                    world[thisObject.id].transform.position = thisObject.getPositionVector();
                    world[thisObject.id].transform.eulerAngles = thisObject.getRotationVector();
                }
                else
                {
                     GameObject newThing = createObjectFromJSONNode(thisObject);
                    if (newThing != null)
                    {
                        world[thisObject.id] = newThing;
                    
                    }
                }

               



            }
              


      

            sliderInput.value = 0;
            
            yield return new WaitForSecondsRealtime(1); // safety margin

            fadeScreenToBlack(false);



            yield return new WaitForSecondsRealtime(delay_ms / 1000);


            fadeScreenToBlack(true);
            yield return new WaitForSecondsRealtime(.2f); // wait for fade

            canvasInput.enabled = true;


            if (useHMD) {
                // giving the user the option to move the slider, waiting until trigger pressed
                while (!bTriggerPulled) { // wait for user input
                    Vector2 vSlider = MoveSlider.GetAxis(handType);
                    // Debug.Log("x: " + vSlider.x.ToString() + ", y" + vSlider.y.ToString());
                    sliderInput.value = sliderInput.value + vSlider.y;
                    yield return null;
                }
            } else {
                while (!Keyboard.current.enterKey.wasPressedThisFrame) {

                    yield return null;
                }
            }

            // SAVE DATA HERE....

            canvasInput.enabled = false;
        }



        //hmdRecord.StartRecording();
        //setSceenBlank(false);

        //yield return new WaitForSecondsRealtime(delay_ms / 1000);
        //LogManager.instance.WriteEntry("characters_gazing: " + strCharacterGazing);

        //LogManager.instance.WriteEntry("--------");
        //hmdRecord.WriteHeader();


        //hmdRecord.StopAndWriteData();

        expRunning = false;

        //turnAllHeads("Panel"); // make sure to be ready for the next round

        //menuManager.gotoThanks();

        ////--setSceenBlank(true);

        //yield return null;

        if (useHMD) {
            rig.transform.position = canvasUI.transform.position;
            rig.transform.position = new Vector3(rig.transform.position.x - 300, rig.transform.position.y, rig.transform.position.z);
            rig.transform.LookAt(canvasUI.transform);
        }

        fadeScreenToBlack(false);




    }

    void turnAllHeads(string strTarget) {
        //if (m_ShowDebugMainController) {
        //    print("SimpleHeadCtrl::turnAllHeads");
        //}
        //GameObject target = GameObject.Find(strTarget);
        //if (target != null) {
        //    Vector3 targetPos = target.transform.position;
        //    foreach (GameObject c in lCharacters) {
        //        //--Debug.Log("# item: " + c);
        //        charControl cc = (charControl)c.GetComponent(typeof(charControl));
        //        cc.setGazeTarget(targetPos);
        //    }
        //} else {
        //    Debug.Log("ERROR: Target not found: " + strTarget);
        //}
    }



    public void StartExperimentCoroutine() {
        UnityEngine.Debug.Log("MainController::StartExperimentCoroutine()");
        if (!expRunning) {
            StartCoroutine(RunExperiment());
        }
    }


    IEnumerator DelayExperimentStart() {
        UnityEngine.Debug.Log("+++++START EXPERIMENT IN 7 SECONDS+++++");

        yield return new WaitForSecondsRealtime(7);

        if (!expRunning) {
            StartCoroutine(RunExperiment());
        }

    }



    void resetAllHeads() {
        //foreach (GameObject c in lCharacters) {
        //    charControl cc = (charControl)c.GetComponent(typeof(charControl));
        //    cc.resetGaze();
        //}
    }

    void toggleBlankScreen() {
        if (!bBlank) {
            canvasUI.enabled = true;
            StartCoroutine(FadeInOut(true));
            // resetAllHeads();
            bBlank = true;
        } else {
            canvasUI.enabled = false;
            StartCoroutine(FadeInOut(false));
            bBlank = false;
        }
    }


    public IEnumerator FadeInOut(bool bToBlack) {

        float fadeSpeed = .5f;
        float fadeAmount;
        float t = 0.0f;

        Image img = canvasBlocker.GetComponentInChildren<Image>();
        if (bToBlack) {
            UnityEngine.Debug.Log("Fade TO Black");
            while (img.color.a < 1) {
                t += fadeSpeed * Time.deltaTime;
                fadeAmount = Mathf.Lerp(img.color.a, 1, t);
                //Debug.Log(fadeAmount);
                Color cc = new Color(0, 0, 0, fadeAmount); /* we cannot set alpha directly, that's why define a new color.... */
                img.color = cc;
                yield return null;
            }
        } else {
            UnityEngine.Debug.Log("Fade FROM Black");

            while (img.color.a > 0) {
                t += fadeSpeed * Time.deltaTime;
                fadeAmount = Mathf.Lerp(img.color.a, 0, t);
                //Debug.Log(fadeAmount);
                Color cc = new Color(0, 0, 0, fadeAmount); /* we cannot set alpha directly, that's why define a new color.... */
                img.color = cc;
                yield return null;
            }

        }
    }

    private void setScreenBlack(bool _bBlack) {

        if (_bBlack) {
            if (m_ShowDebugMainController) {
                print("setSceenBlank::black");
            }
            Image img = canvasBlocker.GetComponentInChildren<Image>();
            Color cc = new Color(0, 0, 0, 1);
            img.color = cc;
            bBlank = true;
        } else {
            if (m_ShowDebugMainController) {
                print("setSceenBlank::unbanck");
            }
            Image img = canvasBlocker.GetComponentInChildren<Image>();
            Color cc = new Color(0, 0, 0, 0);
            img.color = cc;
            bBlank = false;
        }
    }



    private void fadeScreenToBlack(bool _bBlanck) {
        if (_bBlanck) {
            if (m_ShowDebugMainController) {
                print("fadeScreenToBack::black");
            }
            StartCoroutine(FadeInOut(true)); // toBlack
            //--resetAllHeads();
            bBlank = true;
			canvasUI.enabled = true;

        } else {
            if (m_ShowDebugMainController) {
                print("fadeScreenToBack::unblack");
            }

            StartCoroutine(FadeInOut(false));
            bBlank = false;
			canvasUI.enabled = false;

        }
    }
}
