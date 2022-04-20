#include <iostream>
#include <vector>
#include <cstring>

using namespace std;

struct flow_node {
    vector<struct edge> inbound_edges;
    vector<struct edge> outbound_edges;
    int name;
    int balance;
};

struct edge {
    struct flow_node *from, *to;
    int lower_bound;
    int upper_bound;
    int flow;
};

struct customer {
    int lower_bound;
    int upper_bound;
    vector<int> bought_products;
};

int number_of_customers = 0;
int number_of_products = 0;

vector <struct customer> customers;
vector <int> products;

void load (char * input_path){
    FILE * f = fopen(input_path, "r");

    if (f == nullptr){
        cout << "input file not found\n";
        return ;
    }
    fscanf(f, "%i %i", &number_of_customers, &number_of_products);
    for(int i = 0; i<number_of_customers; i++){
        struct customer temp;
        fscanf(f, " %i %i", &temp.lower_bound, &temp.upper_bound);
        char c;
        while ((c = fgetc(f)) != '\n'){
            int t;
            fscanf(f, "%i", &t);
            temp.bought_products.push_back(t-1);
        }
        customers.push_back(temp);
    }
    for (int i = 0; i<number_of_products; i++){
        int temp;
        fscanf(f,"%i", &temp);
        products.push_back(temp);
    }
    fclose(f);
}

void out(char * output_file){
    FILE * f = fopen(output_file, "w+");

    if (f == nullptr){
        cout << "could not create file\n";
        return ;
    }

    fprintf(f, "%i %i\n", number_of_customers, number_of_products);

    for (const auto & c : customers){
        fprintf(f, "%i %i", c.lower_bound, c.upper_bound);
        for(auto p : c.bought_products){
            fprintf(f, " %i", p);
        }
        fprintf(f, "\n");
    }
    for (int i = 0; i<number_of_products; i++){
        fprintf(f, "%i ", products[i]);
    }
    fprintf(f, "\n");
    fclose(f);
}

void print_graph(struct flow_node & s, struct flow_node & t, struct flow_node * customer_nodes, struct flow_node * product_nodes){
    int name = 10;
    s.name = -1;
    t.name = -2;
    for (int i = 0; i < number_of_customers; ++i){
        customer_nodes[i].name = name++;
    }
    name = 20;
    for (int i = 0; i < number_of_products; ++i){
        product_nodes[i].name = name++;
    }

    cout << "---- s start -----\n";
    for (auto e : s.outbound_edges){
        cout << e.lower_bound << " " << e.upper_bound << " " << e.to->balance <<"\n";
    }
    cout << "---- cust start -----\n";
    for (int i = 0; i < number_of_customers; ++i) {
        for (auto e: customer_nodes[i].outbound_edges) {
            cout << e.lower_bound << " " << e.upper_bound << " " << e.to->balance <<"\n";
        }
    }
    cout << "---- prod start -----\n";
    for (int i = 0; i < number_of_products; ++i) {
        for (auto e: product_nodes[i].outbound_edges) {
            cout << e.lower_bound << " " << e.upper_bound << " " << e.to->balance <<"\n";
        }
    }
}

void compute_balance(struct flow_node & n){
    int sum_inbound = 0, sum_outbound = 0;
    for(const auto & e : n.inbound_edges){
        sum_inbound += e.lower_bound;
    }
    cout << sum_inbound << endl;
    for(const auto & e : n.outbound_edges){
        sum_outbound += e.lower_bound;
    }
    cout << sum_inbound << endl;
    n.balance = sum_inbound-sum_outbound;
    cout << n.balance << endl;
}

int main(int argc, char** argv){
    if (argc < 3) {
        cout << "need 2 arguments: ./program <input path> <output path>\n";
    }
    load(argv[1]);

    struct flow_node s;
    struct flow_node t;
//    vector<struct flow_node> customer_nodes;
//    vector<struct flow_node> product_nodes;
    struct flow_node customer_nodes [number_of_customers];
    struct flow_node product_nodes [number_of_products];

    for (int i = 0; i < number_of_customers; i++){
        struct edge e;
        e.lower_bound = customers[i].lower_bound;
        e.upper_bound = customers[i].upper_bound;
        e.flow = -1;
        e.from = &s;
        e.to = &customer_nodes[i];
        s.outbound_edges.push_back(e);
        customer_nodes[i].inbound_edges.push_back(e);
        for (auto u : customers[i].bought_products){
            struct edge ee;
            ee.lower_bound = 0;
            ee.upper_bound = 1;
            ee.flow = -1;
            ee.from = &customer_nodes[i];
            ee.to = &product_nodes[u];
            customer_nodes[i].outbound_edges.push_back(ee);
            product_nodes[u].inbound_edges.push_back(ee);
        }
    }
    for (int i = 0; i < number_of_products; i++){
        struct edge e;
        e.from = &product_nodes[i];
        e.to = &t;
        e.lower_bound = products[i];
        e.upper_bound = INT32_MAX;
        e.flow = -1;
        t.inbound_edges.push_back(e);
        product_nodes[i].outbound_edges.push_back(e);
    }
    //print_graph(s,t,customer_nodes,product_nodes);

    //Finding initial flow

    struct flow_node s1 = s;
    struct flow_node t1 = t;

    struct flow_node customer_nodes_1 [number_of_customers];
    for (int i = 0; i < number_of_customers; i++){
        customer_nodes_1[i] = customer_nodes[i];
    }
    struct flow_node product_nodes_1 [number_of_products];
    for (int i = 0; i < number_of_products; ++i) {
        product_nodes_1[i] = product_nodes[i];
    }

    //print_graph(s1,t1,customer_nodes_1,product_nodes_1);

    struct edge overflow_edge;
    overflow_edge.lower_bound = 0;
    overflow_edge.upper_bound = INT32_MAX;
    overflow_edge.from = &t1;
    overflow_edge.to = &s1;
    t1.outbound_edges.push_back(overflow_edge);
    s1.inbound_edges.push_back(overflow_edge);

    compute_balance(s1);
    cout << s1.balance << endl;
    cout << "-----" << endl;
    compute_balance(t1);
    for (auto & i : customer_nodes_1){
        compute_balance(i);
    }
    for (auto & i : product_nodes_1){
        compute_balance(i);
    }
    cout << "-----" << endl;

    for (auto & i : product_nodes_1){
        cout << i.balance << endl;
    }
    cout << "-----" << endl;

    print_graph(s1,t1,customer_nodes_1,product_nodes_1);


    out(argv[2]);
    return 0;
}