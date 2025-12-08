#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include <grpcpp/grpcpp.h>
#include "leaf_service.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using leafservice::LeafService;
using leafservice::LeafRequest;
using leafservice::PathResponse;
using leafservice::PathRequest;
using leafservice::EmptyResponse;

class LeafServiceClient {
public:
    LeafServiceClient(std::shared_ptr<Channel> channel)
        : stub_(LeafService::NewStub(channel)) {}

    // Send a leaf and receive a list of strings
    std::vector<std::string> ProcessLeaf(int leaf) {
        LeafRequest request;
        request.set_leaf(leaf);
        PathResponse response;
        ClientContext context;

        Status status = stub_->ProcessLeaf(&context, request, &response);
        if (!status.ok()) {
            std::cout << "ProcessLeaf RPC failed." << std::endl;
            return {};
        }

        return { response.strings().begin(), response.strings().end() };
    }

    // Send a list of strings, no response needed
    void SendPath(const std::vector<std::string>& strings) {
        PathRequest request;
        for (const auto& str : strings) {
            request.add_strings(str);
        }
        EmptyResponse response;
        ClientContext context;

        Status status = stub_->SendPath(&context, request, &response);
        if (!status.ok()) {
            std::cout << "SendPath RPC failed." << std::endl;
        }
        std::cout << "skran" << std::endl;
    }

private:
    std::unique_ptr<LeafService::Stub> stub_;
};

int main(int argc, char** argv) {
    LeafServiceClient client(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
    int leaf = 5;  // Example leaf value
    std::vector<std::string> strings = client.ProcessLeaf(leaf);
    for (const auto& str : strings) {
        std::cout << str << "  " << std::endl;
    }

    // Sending a list of strings back
    client.SendPath(strings);

    std::cout << "im out" << std::endl;
 
    return 0;
}
