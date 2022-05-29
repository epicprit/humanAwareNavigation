using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
//using UnityEngine.PhysicsModule;



public class MenuManager : MonoBehaviour {


    // Start is called before the first frame update
    void Start() {
    }



    public void ButtonClicked(string buttonName) {
        //Debug.Log("MenuManager::Button clicked = " + buttonName);


        switch (buttonName) {
            case "btn_Instructions":
                Debug.Log("case:btn_Instructions");
                break;
            case "btn_Quit":
                Debug.Log("case:btn_Quit");
                Application.Quit();
                break;
            case "btn_Reset":
                Debug.Log("case:btn_Reset");
                break;
            default:
                break;

        }

    }


}
