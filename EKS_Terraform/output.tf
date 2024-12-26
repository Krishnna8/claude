output "cluster_id" {
  value = aws_eks_cluster.krishnatest.id
}

output "node_group_id" {
  value = aws_eks_node_group.krishnatest.id
}

output "vpc_id" {
  value = aws_vpc.my_eks_cluster_vpc.id
}

output "subnet_ids" {
  value = aws_subnet.krishnatest_subnet[*].id
}
