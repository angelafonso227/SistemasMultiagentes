using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransform : MonoBehaviour
{
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;
    [SerializeField] float speed = 1.0f;
    [SerializeField] bool recto = true;
    [SerializeField] bool rotar = true;


    Mesh mesh;
    Vector3[] baseVertices;
    Vector3[] newVertices;

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
    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        // Calcular el desplazamiento en el eje x utilizando una función seno para un movimiento suave
        float xDisplacement = Mathf.Sin(Time.time * speed);


        // Matriz de traslación en función del tiempo multiplicado por el desplazamiento
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);

        // Matriz de rotación en función del tiempo multiplicado por el ángulo y el eje de rotación
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle * Time.time, rotationAxis);

        // Matriz para trasladar al origen
        Matrix4x4 posOrigin = HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);

        // Matriz para trasladar de nuevo al objeto a su posición original
        Matrix4x4 posObject = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);

        // Matriz compuesta de traslación y rotación
        Matrix4x4 composite = move * rotate;

        Matrix4x4 composite1 = move * posObject * posOrigin;

        // Imprimir la matriz compuesta
        print(composite);

        if (rotar == true){
            // Aplicar la transformación a cada vértice del objeto
            for (int i = 0; i < newVertices.Length; i++)
            {
                // Crear un vector temporal con las coordenadas del vértice original
                Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
                // Aplicar la transformación a cada vértice
                newVertices[i] = composite * temp;

            }
        }
        
        if (recto == true)
        {
            for (int i = 0; i < newVertices.Length; i++)
            { 
                // Crear un vector temporal con las coordenadas del vértice original
                Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
                // Aplicar la transformación a cada vértice
                newVertices[i] = composite1 * temp;

            }
        }

        // Reemplazar los vértices en el objeto de malla
        mesh.vertices = newVertices;

        // Recalcular las normales de la malla
        mesh.RecalculateNormals();
    }
}