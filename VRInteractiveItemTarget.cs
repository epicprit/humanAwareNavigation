using System.Collections;
using UnityEngine;
using System;



public class VRInteractiveItemTarget : VRInteractiveItemBaseclass {

    

    public AudioSource audioCorrect;
    public AudioSource audioWrong;
    private bool ErrorSound;
    private GameObject goFire;

    public const string strSettingAudioFeeback = "Audio Error Feedback";


    public static bool IsEnabledAudioFeedback {
        get { return Convert.ToBoolean(PlayerPrefs.GetInt(strSettingAudioFeeback)); }
        set { PlayerPrefs.SetInt(strSettingAudioFeeback, Convert.ToInt16(value)); }

    }


    void Start() {
        ErrorSound = IsEnabledAudioFeedback;
        goFire = transform.Find("FirePS").gameObject;
    }

    public override void FocusIn() {
        //      Debug.Log("VRInteractiveItemTarget::focusIn: " + gameObject.name);
        bHasFocus = true;

        if (goFire) {
            StartCoroutine(DimLights());
        }

        if (MainController.expRunning /* -- && !MainController.expPaused */) {
            LogManager.instance.WriteTimeStampedEntry("TargetHit: " + gameObject.name);

            if (ErrorSound) {
				if (MainController.currentTargetPpn == "choose") {
					audioCorrect.Play();
                } else if (MainController.currentTargetPpn != name) {
                    audioWrong.Play();
                } else {
					audioCorrect.Play();
				}
            }
        }
    }

    public override void FocusOut() {
        //        Debug.Log("VRInteractiveItemTarget::focusOut: " + gameObject.name);
        bHasFocus = false;
    }


    public void TurnFireOn(bool b) {
        if (b) {
            goFire.GetComponent<ParticleSystem>().Play();
            goFire.GetComponent<Light>().intensity = 1.5f;
        } else {
            StartCoroutine(DimLights());
        }
    }

    IEnumerator DimLights() {
 //       Debug.Log("VRInteractiveItemTarget::DimLights:");
        if (goFire) {

            float fIntensity = goFire.GetComponent<Light>().intensity; // avoid turning it on... 1.5f;

            while (fIntensity > 0.21) {
                fIntensity = Mathf.Lerp(fIntensity, 0.2f, .15f);
                goFire.GetComponent<Light>().intensity = fIntensity;
                // print("fIntensity: " + fIntensity);
                yield return new WaitForSecondsRealtime(500/1000);

            }
            goFire.GetComponent<Light>().intensity = 0f;
            //  yield return new WaitForSecondsRealtime(2);
            goFire.GetComponent<ParticleSystem>().Stop();
        }
    }

}