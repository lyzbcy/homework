using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Follow : MonoBehaviour
{

    public Transform player1;
    public Transform player2;

    private Camera camera;
    private Vector3 offset;


    // 最小和最大距离对应的摄像头旋转角度
    private const float minDistance = 25f;
    private const float maxDistance = 50f;
    private const float minRotationX = 57.58f;
    private const float maxRotationX = 90f;


    // Start is called before the first frame update
    void Start()
    {
        offset = transform.position - (player1.position + player2.position) / 2;
        camera = this.GetComponent<Camera>();
    }

    // Update is called once per frame
    void Update()
    {
        if (player1 == null || player2 == null) return;
        transform.position = (player1.position + player2.position) / 2 + offset;
        float distance = Vector3.Distance(player1.position, player2.position);

        if (distance <= 5f) return;

       
        float size = distance * 0.875f;
        camera.orthographicSize = size;


        if (distance > minDistance)
        {
            // 计算新的x旋转角度，使其随着距离增加而增加，直至90度
            float targetRotationX = Mathf.Lerp(minRotationX, maxRotationX, (distance - minDistance) / (maxDistance - minDistance));
            Vector3 currentRotation = transform.rotation.eulerAngles;
            transform.rotation = Quaternion.Euler(targetRotationX, currentRotation.y, currentRotation.z);
        }
        else
        {
            // 当距离小于等于25时，设置x旋转角度为57.58
            Vector3 currentRotation = transform.rotation.eulerAngles;
            transform.rotation = Quaternion.Euler(minRotationX, currentRotation.y, currentRotation.z);
        }

    }
}
