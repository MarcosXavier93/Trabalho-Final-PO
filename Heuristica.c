#include <stdlib.h>
#include <stdio.h>
#include <limits.h>
struct matriz {
    int numero_de_elementos;
    int** elementos;
};
#define TRUE 1
struct nodo {
    int indice_nodo;
    int valor;
};
#define FALSE 0
int calcular_custo(struct matriz, int*);
void caminho_randomico(struct matriz, int*);
void ler_arquivo(struct matriz*, char*);
void printa_caminho(int, int*);
void desenvolve_caminho(struct matriz, int*);
void printa_linha();
void imprimir_matriz(struct matriz);
int main(int argc, char *argv[]) {
    struct matriz m;
    ler_arquivo(&m, "entrada.txt");
    imprimir_matriz(m);
    int *solucao = malloc((m.numero_de_elementos + 1) * sizeof(int));
    desenvolve_caminho(m, solucao);
    printf("Solucao inicial: ");
    printa_caminho(m.numero_de_elementos + 1, solucao);
    int custo_solucao = calcular_custo(m, solucao);
    printf("Custo solução inicial: %d", custo_solucao);
    printa_linha();
    srand(1);
    int *solucao_aleatoria = malloc((m.numero_de_elementos + 1) * sizeof(int));
    for(int i = 0; i < 10; i++) {
        caminho_randomico(m, solucao_aleatoria);
        int custo_solucao_aleatoria = calcular_custo(m, solucao_aleatoria);
        printf("Solucao aleatória: ");
        printa_caminho(m.numero_de_elementos + 1, solucao_aleatoria);
        printf("Custo solução aleatória: %d Kilometros\n", custo_solucao_aleatoria);    }}
void ler_arquivo(struct matriz* m, char* arquivo) {
    FILE* fp = fopen(arquivo, "r");
    fscanf(fp, "%d\n", &m->numero_de_elementos);
    m->elementos = malloc(m->numero_de_elementos * sizeof(int*));
    for(int i = 0; i < m->numero_de_elementos; i++) {
        m->elementos[i] = malloc(m->numero_de_elementos * sizeof(int));
        for(int j = 0; j < m->numero_de_elementos; j++) {
            fscanf(fp, "%d ", &m->elementos[i][j]);
        }    }
    fclose(fp);}
int calcular_custo(struct matriz m, int* caminho) {
    int custo = 0;
    for(int i = 0; i < m.numero_de_elementos; i++) {
        custo = custo + m.elementos[caminho[i]][caminho[i + 1]];    }
    return custo;}
void desenvolve_caminho(struct matriz m, int* caminho) {
    int *inseridos = malloc(m.numero_de_elementos * sizeof(int));
    for(int i = 0; i < m.numero_de_elementos; i++) {
        inseridos[i] = FALSE;    }
    caminho[0] = 0;
    inseridos[0] = TRUE;
    for(int i = 0; i < m.numero_de_elementos; i++) {
        int valor_referencia = INT_MAX;
        int vizinho_selecionado = 0;
        for(int j = 0; j < m.numero_de_elementos; j++) {
            if(!inseridos[j] && valor_referencia > m.elementos[i][j]) {
                vizinho_selecionado = j;
                valor_referencia = m.elementos[i][j];
            }        }
        caminho[i + 1] = vizinho_selecionado;
        inseridos[vizinho_selecionado] = TRUE;    }
    caminho[m.numero_de_elementos] = 0;
        free(inseridos);}
void caminho_randomico(struct matriz m, int* caminho) {
    int *inseridos = malloc(m.numero_de_elementos * sizeof(int));
    struct nodo *vizinhos = malloc(m.numero_de_elementos * sizeof(struct nodo));
    for(int i = 0; i < m.numero_de_elementos; i++) {
        inseridos[i] = FALSE;    }
    caminho[0] = 0;
    inseridos[0] = TRUE;

    for(int i = 0; i < m.numero_de_elementos; i++) {
        int iv = 0;        for(int j = 0; j < m.numero_de_elementos; j++) {
            if(!inseridos[j]) {
                vizinhos[iv].indice_nodo = j;
                vizinhos[iv].valor = m.elementos[i][j];
                iv++;       }    }
        if(iv == 0) {
            caminho[i + 1] = 0;
        } else {
            int vizinho_selecionado = rand() % iv;
            caminho[i + 1] = vizinhos[vizinho_selecionado].indice_nodo;
            inseridos[vizinhos[vizinho_selecionado].indice_nodo] = TRUE;        } }
    free(inseridos);
    free(vizinhos);}
void imprimir_matriz(struct matriz m) {
    printa_linha();
    printf("Matriz\n\n");
    for(int i = 0; i < m.numero_de_elementos; i++) {
        for(int j = 0; j < m.numero_de_elementos; j++) {
            printf("%d ", m.elementos[i][j]);        }
        printf("\n");    }
    printa_linha();}
void printa_caminho(int n, int* caminho) {
    int i;
    for(i = 0; i < n; i++) {
        printf("%d ", caminho[i]);    }
    printf("\n");}
void printa_linha() {
    int i;
    printf("\n");
    for(i = 0; i < 80; i++) printf("_");
    printf("\n");}