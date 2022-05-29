using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SliderValues : MonoBehaviour
{

    public Text txtMin;
    public Text txtMax;
    public Text txtVal;

    // Start is called before the first frame update
    void Start()
    {

        Slider slider = GetComponent<Slider>();
        txtMin.text = slider.minValue.ToString();
        txtMax.text = slider.maxValue.ToString();
        //keep empty 
        txtVal.text = ""; // slider.value.ToString();
        slider.onValueChanged.AddListener(delegate { ValueChangeCheck(); });

    }

    // Invoked when the value of the slider changes.
    public void ValueChangeCheck() {
        Slider slider = GetComponent<Slider>();
         txtVal.text = slider.value.ToString();
    }


}
