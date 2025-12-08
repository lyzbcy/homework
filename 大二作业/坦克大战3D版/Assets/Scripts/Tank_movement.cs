using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tank_movement : MonoBehaviour
{
    public float speed = 5;     //坦克移动速度
    public float angularSpeed = 10;     //坦克旋转速度
    public float number = 1;            //增加玩家编号
    public AudioClip idleAudio;
    public AudioClip drivingAudio;

    private AudioSource audio;
    private Rigidbody rigidbody;

    void Start()
    {
        rigidbody = this.GetComponent<Rigidbody>();
        audio = this.GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        float v = Input.GetAxis("VerticalP"+number);            //当按下上下箭头时触发
        rigidbody.velocity = transform.forward*v*speed;


        float h = Input.GetAxis("HorizontalP"+number);      //当按下左右箭头时触发
        rigidbody.angularVelocity = transform.up * h * angularSpeed;

        if (Mathf.Abs(h) > 0.1 || Mathf.Abs(v) > 0.1)
        {
            audio.clip = drivingAudio;
            if (audio.isPlaying == false)
                audio.Play();

        }

    }
}
