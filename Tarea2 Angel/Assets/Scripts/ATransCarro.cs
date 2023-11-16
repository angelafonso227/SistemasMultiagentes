using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ATransCarro : MonoBehaviour
{
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;
    Mesh mesh;
    Vector3[] baseVertices;
    Vector3[] newVertices;
    [SerializeField] GameObject FL;
    [SerializeField] GameObject FR;
    [SerializeField] GameObject BL;
    [SerializeField] GameObject BR;
    [SerializeField] bool rotado = false;
    [SerializeField] bool rotado1 = false;
    [SerializeField] bool rotado2 = false;

    // Start is called before the first frame update
    void Start()
    {
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;
        

        // Crear una copia de los vértices originales
        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        FL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
        FR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
        BL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
        BR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
        FL.transform.localScale =  new Vector3(0.3f, 0.3f, 0.3f);
        FR.transform.localScale =  new Vector3(0.3f, 0.3f, 0.3f);
        BL.transform.localScale =  new Vector3(0.3f, 0.3f, 0.3f);
        BR.transform.localScale =  new Vector3(0.3f, 0.3f, 0.3f);
        FL.transform.position = new Vector3(1.45f, 0.3f, 1.0f);
        FR.transform.position = new Vector3(1.45f, 0.3f, -1.0f);
        BL.transform.position = new Vector3(-1.225f, 0.3f, 1.0f);
        BR.transform.position = new Vector3(-1.225f, 0.3f, -1.0f);

    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        // Matriz de traslación en función del tiempo multiplicado por el desplazamiento
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);

        // Matriz de rotación en función del tiempo multiplicado por el ángulo y el eje de rotación
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle * Time.time, rotationAxis);

        // // Matriz para trasladar al origen
        // Matrix4x4 posOrigin = HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);
        // Matrix4x4 posObject = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);

        // Matriz compuesta de traslación y rotación
        Matrix4x4 composite = move * rotate;

            // Aplicar la transformación a cada vértice del objeto
        for (int i = 0; i < newVertices.Length; i++)
        {
            // Crear un vector temporal con las coordenadas del vértice original
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            // Aplicar la transformación a cada vértice usando la matriz compuesta
            newVertices[i] = composite * temp;
        }
        

        // Reemplazar los vértices en el objeto de malla
        mesh.vertices = newVertices;

        // Recalcular las normales de la malla
        mesh.RecalculateNormals();

        if (Time.time >= 3 && rotado==false)
        {
            FL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            FR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            BL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            BR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            FL.transform.position = new Vector3(4.0f, 0.3f, 1.225f);
            FR.transform.position = new Vector3(2.0f, 0.3f, 1.225f);
            BL.transform.position = new Vector3(4.0f, 0.3f, -1.455f);
            BR.transform.position = new Vector3(2.0f, 0.3f, -1.455f);
            transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            transform.position = new Vector3(3.0f, 0.0f, 0.0f);
            rotado=true;

            for (int i = 0; i < newVertices.Length; i++)
            {
                // Crear un vector temporal con las coordenadas del vértice original
                Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
                // Aplicar la transformación a cada vértice usando la matriz compuesta
                newVertices[i] = - (composite * temp);
            }
        }

        if (Time.time >= 6 && rotado1==false)
        {
            FL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            FR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            BL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            BR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            FL.transform.position = new Vector3(8.55f, 0.3f, -6.0f);
            FR.transform.position = new Vector3(8.55f, 0.3f, -8.0f);
            BL.transform.position = new Vector3(11.225f, 0.3f, -6.0f);
            BR.transform.position = new Vector3(11.225f, 0.3f, -8.0f);
            transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            transform.position = new Vector3(10.0f, 0.0f, -7.0f);
            
            rotado1=true;

            for (int i = 0; i < newVertices.Length; i++)
            {
                // Crear un vector temporal con las coordenadas del vértice original
                Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
                // Aplicar la transformación a cada vértice usando la matriz compuesta
                newVertices[i] = - (composite * temp);
            }
        }

        if (Time.time >= 9 && rotado2==false)
        {
            FL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            FR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            BL.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            BR.transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            FL.transform.position = new Vector3(1.0f, 0.3f, -11.3f);
            FR.transform.position = new Vector3(-1.0f, 0.3f, -11.3f);
            BL.transform.position = new Vector3(1.0f, 0.3f, -14.0f);
            BR.transform.position = new Vector3(-1.0f, 0.3f, -14.0f);
            transform.rotation *= Quaternion.Euler(0.0f, 90.0f, 0.0f);
            transform.position = new Vector3(0.0f, 0.0f, -12.75f);
            rotado2=true;

            for (int i = 0; i < newVertices.Length; i++)
            {
                // Crear un vector temporal con las coordenadas del vértice original
                Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
                // Aplicar la transformación a cada vértice usando la matriz compuesta
                newVertices[i] = - (composite * temp);
            }
        }

    }
}
