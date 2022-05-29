using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class btnResetCounter : MonoBehaviour {
    public Button yourButton;

    void Start() {
        Button btn = yourButton.GetComponent<Button>();
        btn.onClick.AddListener(TaskOnClick);
    }

    void TaskOnClick() {
        Debug.Log("btnResetCounter::TaskOnClick()");
        PlayerPrefs.SetInt("currentTrial", 0);
        //int iCurrentTrial = PlayerPrefs.GetInt("currentTrial");
    }
}