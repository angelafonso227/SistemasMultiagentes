using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ATransformTodo : MonoBehaviour
{
    private bool rotateishon = false;
    [SerializeField] Vector3 displacement;
    [SerializeField] Vector3 displacementBR;
    [SerializeField] Vector3 displacementFR;
    
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;
    [SerializeField] GameObject FL;
    [SerializeField] GameObject FR;
    [SerializeField] GameObject BL;
    [SerializeField] GameObject BR;
    Mesh mesh; 
    Mesh meshBR;
    Mesh meshFR;
    Vector3[] baseVertices;
    Vector3[] newVertices;    
    Vector3[] baseVerticesBR;
    Vector3[] newVerticesBR;
    Vector3[] baseVerticesFR;
    Vector3[] newVerticesFR;

    // Start is called before the first frame update
    void Start()
    {
        mesh = GameObject.Find("Nave").GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;

        // Crear una copia de los vértices originales
        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        meshBR = GameObject.Find("BR").GetComponentInChildren<MeshFilter>().mesh;
        baseVerticesBR = meshBR.vertices;

        // Crear una copia de los vértices originales
        newVerticesBR = new Vector3[baseVerticesBR.Length];
        for (int i = 0; i < baseVerticesBR.Length; i++)
        {
            newVerticesBR[i] = baseVerticesBR[i];
        }

        meshFR = GameObject.Find("FR").GetComponentInChildren<MeshFilter>().mesh;
        baseVerticesFR = meshFR.vertices;

        // Crear una copia de los vértices originales
        newVerticesFR = new Vector3[baseVerticesFR.Length];
        for (int i = 0; i < baseVerticesFR.Length; i++)
        {
            newVerticesFR[i] = baseVerticesFR[i];
        }

    }

    // Update is called once per frame
    void Update()
    {        
        if (!rotateishon)
        {
            DoTransform();
            rotateishon = true;
        }
    }

    void DoTransform()
    {
        // Matriz de traslación en función del tiempo multiplicado por el desplazamiento
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);
        Matrix4x4 moveBR = HW_Transforms.TranslationMat(displacementBR.x * Time.time, displacementBR.y * Time.time, displacementBR.z * Time.time);
        Matrix4x4 moveFR = HW_Transforms.TranslationMat(displacementFR.x * Time.time, displacementFR.y * Time.time, displacementFR.z * Time.time);

        // Matriz de rotación en función del tiempo multiplicado por el ángulo y el eje de rotación
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle * Time.time, rotationAxis);

        // Matriz para trasladar al origen
        Matrix4x4 posOrigin = HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);
        Matrix4x4 posOriginBR = HW_Transforms.TranslationMat(-displacementBR.x, -displacementBR.y, -displacementBR.z);
        Matrix4x4 posOriginFR = HW_Transforms.TranslationMat(-displacementFR.x, -displacementFR.y, -displacementFR.z);

        // Matriz para trasladar de nuevo al objeto a su posición original
        Matrix4x4 posObject = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);
        Matrix4x4 posObjectBR = HW_Transforms.TranslationMat(displacementBR.x, displacementBR.y, displacementBR.z);
        Matrix4x4 posObjectFR = HW_Transforms.TranslationMat(displacementFR.x, displacementFR.y, displacementFR.z);


        // Matriz compuesta de traslación y rotación

        Matrix4x4 composite = move * posObject * posOrigin;

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


        Matrix4x4 camavingaBR = moveBR * posObjectBR * posOriginBR;
        Matrix4x4 camavingaFR = moveFR * posObjectFR * posOriginFR;


        
        for (int i = 0; i < newVertices.Length; i++)
        { 
            // Crear un vector temporal con las coordenadas del vértice original
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            // Aplicar la transformación a cada vértice
            newVertices[i] = composite * temp;
        }

        for (int i = 0; i < newVerticesBR.Length; i++)
        { 
            // Crear un vector temporal con las coordenadas del vértice original
            Vector4 tempBR = new Vector4(baseVerticesBR[i].x, baseVerticesBR[i].y, baseVerticesBR[i].z, 1);
            // Aplicar la transformación a cada vértice
            newVerticesBR[i] = camavingaBR * tempBR;
        }

        for (int i = 0; i < newVerticesFR.Length; i++)
        { 
            // Crear un vector temporal con las coordenadas del vértice original
            Vector4 tempFR = new Vector4(baseVerticesFR[i].x, baseVerticesFR[i].y, baseVerticesFR[i].z, 1);
            // Aplicar la transformación a cada vértice
            newVerticesFR[i] = camavingaFR * tempFR;
        }
        

        // Reemplazar los vértices en el objeto de malla
        mesh.vertices = newVertices;
        meshBR.vertices = newVerticesBR;
        meshFR.vertices = newVerticesFR;

        // Recalcular las normales de la malla
        mesh.RecalculateNormals();
        meshBR.RecalculateNormals();
        meshFR.RecalculateNormals();
    }
}
