"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { PlusCircle, Trash2 } from "lucide-react"
import { useLocalStorage } from "@/hooks/use-local-storage"
import type { Category } from "@/lib/types"
import initialCategories from "@/data/categories.json"
import { useToast } from "@/hooks/use-toast"
import { SidebarTrigger } from "@/components/ui/sidebar"

export default function CategoriesPage() {
  const [categories, setCategories] = useLocalStorage<Category[]>("categories", initialCategories)
  const [newCategoryName, setNewCategoryName] = useState("")
  const [newCategorySolutions, setNewCategorySolutions] = useState("")
  const { toast } = useToast()

  const handleAddCategory = () => {
    if (!newCategoryName.trim()) {
      toast({
        title: "Error",
        description: "Category name cannot be empty.",
        variant: "destructive",
      })
      return
    }
    const newCategory: Category = {
      id: `cat-${Date.now()}`,
      name: newCategoryName,
      solutions: newCategorySolutions.split("\n").filter((s) => s.trim() !== ""),
    }
    setCategories([...categories, newCategory])
    setNewCategoryName("")
    setNewCategorySolutions("")
    toast({
      title: "Category Added",
      description: `Category "${newCategoryName}" has been added.`,
    })
  }

  const handleDeleteCategory = (id: string) => {
    const categoryName = categories.find((c) => c.id === id)?.name
    setCategories(categories.filter((c) => c.id !== id))
    toast({
      title: "Category Deleted",
      description: `Category "${categoryName}" has been deleted.`,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <SidebarTrigger />
        <h1 className="text-2xl font-semibold">Manage Categories</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Add New Category</CardTitle>
          <CardDescription>Create a new category and add potential solutions.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="new-category-name">Category Name</Label>
            <Input
              id="new-category-name"
              value={newCategoryName}
              onChange={(e) => setNewCategoryName(e.target.value)}
              placeholder="e.g., Subscription Issues"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="new-category-solutions">Solutions (one per line)</Label>
            <Textarea
              id="new-category-solutions"
              value={newCategorySolutions}
              onChange={(e) => setNewCategorySolutions(e.target.value)}
              placeholder="e.g., Check payment history for duplicates."
              rows={4}
            />
          </div>
          <Button onClick={handleAddCategory}>
            <PlusCircle className="mr-2 h-4 w-4" />
            Add Category
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Existing Categories</CardTitle>
          <CardDescription>View and manage current ticket categories.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {categories.map((category) => (
            <Card key={category.id} className="p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold">{category.name}</h3>
                  <ul className="list-disc list-inside text-sm text-muted-foreground mt-2">
                    {category.solutions.map((solution, index) => (
                      <li key={index}>{solution}</li>
                    ))}
                    {category.solutions.length === 0 && <li className="text-xs italic">No solutions defined.</li>}
                  </ul>
                </div>
                <Button variant="ghost" size="icon" onClick={() => handleDeleteCategory(category.id)}>
                  <Trash2 className="h-4 w-4" />
                  <span className="sr-only">Delete category</span>
                </Button>
              </div>
            </Card>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
