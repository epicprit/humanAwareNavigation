using UnityEngine;
using System.Collections;


public class Loader : MonoBehaviour
{
    public GameObject logManager; //LogManager prefab to instantiate.
   

    void Awake()
    {
        print("Loader:Awake");
        //Check if a LogManager has already been assigned to static variable LogManager.instance or if it's still null
        if (LogManager.instance == null)
        {
            //Instantiate gameManager prefab
            Instantiate(logManager);
        }



    }
}