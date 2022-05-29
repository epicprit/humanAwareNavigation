using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class HMDRecord : MonoBehaviour {

    List<string> data = new List<string>();

    private bool recording;

    public string[] header;

    const string format = "0.####";

    // Use this for initialization
    void Start() {
        header = new string[] {
                "time",
				"event",
                "pos_x",
                "pos_y",
                "pos_z",
                "rot_x",
                "rot_y",
                "rot_z"};
    }

    // Update is called once per frame
   // void Update() {
//        RecordRow();
  //  }

    // called by unity just before rendering the frame
    void LateUpdate() {
        RecordRow();
    }

    public string[] customHeader = new string[] { };

    /// <summary>
    /// Records a new row of data at current time.
    /// </summary>
    public void RecordRow() {
        if (recording) {
            Vector3 p = gameObject.transform.position;
            Vector3 r = gameObject.transform.eulerAngles;

            string strData = Time.realtimeSinceStartup.ToString() + ";HMD;" +
            p.x.ToString(format) + ";" +
                p.y.ToString(format) + ";" +
                p.z.ToString(format) + ";" +
                r.x.ToString(format) + ";" +
                r.y.ToString(format) + ";" +
                r.z.ToString(format);

            data.Add(strData);
        }
    }

    ///// <summary>
    ///// Returns current position and rotation values
    ///// </summary>
    ///// <returns></returns>
    //private string[] GetCurrentValues() {
    //    // get position and rotation
    //    Vector3 p = gameObject.transform.position;
    //    Vector3 r = gameObject.transform.eulerAngles;

    //    string format = "0.####";

    //    // return position, rotation (x, y, z) as an array
    //    var values = new string[]
    //    {
    //            p.x.ToString(format),
    //            p.y.ToString(format),
    //            p.z.ToString(format),
    //            r.x.ToString(format),
    //            r.y.ToString(format),
    //            r.z.ToString(format)
    //    };

    //    return values;
    //}


    /// <summary>
    /// Begins recording.
    /// </summary>
    public void StartRecording() {
        data.Clear();
        recording = true;
    }


    /// <summary>
    /// Stops recording.
    /// </summary>
    public void StopAndWriteData() {
        recording = false;
        LogManager.instance.WriteEntry(data);
    }


    public void WriteHeader() {
        LogManager.instance.WriteEntry(string.Join(";", header));
    }


}
