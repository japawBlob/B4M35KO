#include <iostream>
#include <vector>

struct flow_node {

};

struct customer {
    int lower_bound;
    int upper_bound;
    std::vector<int> products;
};

int number_of_customers = 0;
int number_of_products = 0;

int main(int argc, char** argv){
    if (argc < 3) {
        std::cout << "need 2 arguments: ./program <input path> <output path>\n";
    }
    FILE * f = fopen(argv[1], "r");

    if (f == nullptr){
        std::cout << "input file not found\n";
        return 1;
    }

    fscanf(f, "%i %i", &number_of_customers, &number_of_products);

    struct customer customers [number_of_customers];
    int product_demand [number_of_products];


    for(int i = 0; i<number_of_customers; i++){
        fscanf(f, " %i %i", &customers[i].lower_bound, &customers[i].upper_bound);
        char c;
        int counter = 0;
        while ((c = fgetc(f)) != '\n'){
            printf("xxXX__%c__XXxx\n", c);
            int temp;
            fscanf(f, "%i", &temp);
            customers[i].products.push_back(temp);
        }
    }
    for (int i = 0; i<number_of_products; i++){
        fscanf(f,"%i", &product_demand[i]);
    }

    fclose(f);
    f = fopen(argv[2], "w+");

    if (f == nullptr){
        std::cout << "could not create file\n";
        return 1;
    }

    fprintf(f, "%i %i\n", number_of_customers, number_of_products);

    for (auto c : customers){
        fprintf(f, "%i %i", c.lower_bound, c.upper_bound);
        for(auto p : c.products){
            fprintf(f, " %i", p);
        }
        fprintf(f, "\n");
    }
    for (int i = 0; i<number_of_products; i++){
        fprintf(f, "%i ", product_demand[i]);
    }
    fprintf(f, "\n");
    fclose(f);
    return 0;
}